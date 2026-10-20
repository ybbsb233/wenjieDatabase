package cn.edu.learning.service.impl;

import cn.edu.learning.exception.ApiException;
import cn.edu.learning.mapper.*;
import cn.edu.learning.pojo.Models.*;
import cn.edu.learning.service.PracticeService;
import cn.edu.learning.utils.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.*;

@Service
public class PracticeServiceImpl implements PracticeService {
 private final PracticeMapper practices; private final QuestionMapper questions; private final CourseMapper courses;
 public PracticeServiceImpl(PracticeMapper p,QuestionMapper q,CourseMapper c){practices=p;questions=q;courses=c;}
 @Transactional @Override public Object start(User user,Start input){
    long course=Ids.parse(input.courseId()); Long chapter=Ids.optional(input.chapterId()),knowledge=Ids.optional(input.knowledgeId());
    if(courses.courseExists(course)==0)throw new ApiException(404,"课程不存在");
    if(chapter!=null&&courses.chapterMatches(chapter,course)==0)throw new ApiException(400,"章节不属于所选课程");
    if(knowledge!=null&&courses.knowledgeMatches(knowledge,course,chapter)==0)throw new ApiException(400,"知识点不属于筛选范围");
    List<Question> pool=new ArrayList<>(questions.candidates(course,chapter,knowledge));Collections.shuffle(pool);
    return create(user,course,"NORMAL",pool.subList(0,Math.min(input.count(),pool.size())),input.count());
 }
 @Transactional @Override public Object fromWrong(User user,WrongStart input){
    long course=Ids.parse(input.courseId()); Set<Long> ids=new HashSet<>(); List<Question> pool=new ArrayList<>();
    for(String raw:input.questionIds()){
        long id=Ids.parse(raw); if(!ids.add(id))throw new ApiException(400,"错题不能重复");
        Question q=questions.byId(id);if(q==null||q.courseId()!=course||questions.wasWrong(user.id(),id)==0)throw new ApiException(400,"题目不属于本人所选课程的错题");pool.add(q);
    }
    return create(user,course,"WRONG",pool,pool.size());
 }
 private Object create(User user,long course,String type,List<Question> pool,int requested){
    return create(user,course,type,pool,requested,null);
 }
 private Object create(User user,long course,String type,List<Question> pool,int requested,Long chapterId){
    if(pool.isEmpty())throw new ApiException(400,"没有符合条件的题目");
    Map<String,Object> row=new HashMap<>();row.put("studentId",user.id());row.put("courseId",course);row.put("chapterId",chapterId);row.put("sourceType",type);row.put("questionCount",pool.size());practices.insert(row);
    long id=((Number)row.get("id")).longValue();int order=1;for(Question q:pool)practices.insertItem(id,q.id(),order++,AnswerRules.shuffle(q.questionType()));
    return Map.of("practiceId",Long.toString(id),"requestedCount",requested,"actualCount",pool.size());
 }
 @Override public Object chapterSets(User user,long courseId){
    if(courses.courseExists(courseId)==0)throw new ApiException(404,"课程不存在");
    return practices.chapterSets(user.id(),courseId);
 }
 @Transactional @Override public Object startChapter(User user,long chapterId){
    // The catalog validates current chapters. Fixed sets keep canonical question order.
    for(Map<String,Object> course:courses.courses()){
        long courseId=Ids.parse(course.get("id").toString());
        if(courses.chapterMatches(chapterId,courseId)==1){
            List<Question> pool=questions.candidates(courseId,chapterId,null);
            if(pool.size()!=20)throw new ApiException(409,"章节练习必须包含20道题，请检查题库");
            return create(user,courseId,"CHAPTER",pool,20,chapterId);
        }
    }
    throw new ApiException(404,"章节练习不存在");
 }
 private Practice owned(User user,Practice p){
    if(p==null||(!user.role().equals("ADMIN")&&!p.studentId().equals(user.id())))throw new ApiException(404,"练习不存在");return p;
 }
 @Override public Object questions(User user,long id){
    Practice p=owned(user,practices.byId(id));if(!p.status().equals("IN_PROGRESS"))throw new ApiException(409,"练习已提交，请查看结果");
    List<QuestionView> views=new ArrayList<>();for(Item i:practices.items(id)){Question q=questions.byId(i.questionId());views.add(new QuestionView(i.id().toString(),i.orderNo(),q.questionType(),q.stem(),AnswerRules.options(q,i.optionOrder())));}
    return Map.of("practiceId",Long.toString(id),"courseId",p.courseId().toString(),"practiceName",title(p),"questionCount",p.questionCount(),"items",views);
 }
 @Transactional @Override public Object submit(User user,long id,Submit input){
    Practice p=owned(user,practices.lock(id));if(p.status().equals("SUBMITTED"))return score(p);
    List<Item> items=practices.items(id);Map<Long,List<String>> answers=new HashMap<>();Set<Long> allowed=new HashSet<>();for(Item i:items)allowed.add(i.id());
    for(Answer a:input.answers()){long item=Ids.parse(a.itemId());if(!allowed.contains(item)||answers.putIfAbsent(item,a.selectedLabels())!=null)throw new ApiException(400,"答案明细重复或不属于本次练习");}
    int count=0;for(Item i:items){Question q=questions.byId(i.questionId());String selected=AnswerRules.normalize(answers.getOrDefault(i.id(),List.of()),i.optionOrder(),q.questionType());boolean correct=AnswerRules.correct(selected,i.optionOrder(),q.correctAnswer());practices.answer(i.id(),selected,correct?1:0);if(correct)count++;}
    practices.finish(id,count);return score(practices.byId(id));
 }
 private Map<String,Object> score(Practice p){return Map.of("practiceId",p.id().toString(),"questionCount",p.questionCount(),"correctCount",p.correctCount(),"accuracy",AnswerRules.accuracy(p.correctCount(),p.questionCount()));}
 @Override public Object result(User user,long id){
    Practice p=owned(user,practices.byId(id));if(!p.status().equals("SUBMITTED"))throw new ApiException(409,"练习尚未提交");
    List<ResultItem> views=new ArrayList<>();for(Item i:practices.items(id)){Question q=questions.byId(i.questionId());views.add(new ResultItem(i.id().toString(),q.id().toString(),i.orderNo(),q.questionType(),q.stem(),AnswerRules.options(q,i.optionOrder()),AnswerRules.labels(i.selectedAnswer()),AnswerRules.displayedCorrect(q.correctAnswer(),i.optionOrder()),i.isCorrect()==1,q.explanation()));}
    Map<String,Object> result=new HashMap<>(score(p));result.put("courseId",p.courseId().toString());result.put("practiceName",title(p));result.put("studentId",p.studentId().toString());result.put("submittedAt",p.submittedAt());result.put("items",views);return result;
 }
 private String title(Practice p){return p.chapterId()!=null?practices.chapterTitle(p.chapterId())+" · 固定章节练习":p.sourceType().equals("WRONG")?"错题重练":"自主随机练习";}
 @Override public Page<?> history(long studentId,Long courseId,int page,int size){int offset=Ids.offset(page,size);return new Page<>(practices.historyCount(studentId,courseId),practices.history(studentId,courseId,offset,size));}
 @Override public Page<?> allHistory(Long studentId,Long courseId,int page,int size){int offset=Ids.offset(page,size);return new Page<>(practices.allHistoryCount(studentId,courseId),practices.allHistory(studentId,courseId,offset,size));}
}

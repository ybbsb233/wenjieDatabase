package cn.edu.learning.service.impl;
import cn.edu.learning.exception.ApiException;
import cn.edu.learning.mapper.*;
import cn.edu.learning.pojo.Models.Page;
import cn.edu.learning.service.LearningService;
import cn.edu.learning.utils.*;
import org.springframework.stereotype.Service;
import java.util.*;
@Service
public class LearningServiceImpl implements LearningService {
 private final LearningMapper mapper; private final CourseMapper courses;private final UserMapper users;
 public LearningServiceImpl(LearningMapper m,CourseMapper c,UserMapper u){mapper=m;courses=c;users=u;}
 private void course(long id){if(courses.courseExists(id)==0)throw new ApiException(404,"课程不存在");}
 @Override public Object summary(Long studentId){return mapper.summary(studentId);}
 @Override public Object knowledge(Long studentId,long courseId){
    course(courseId);List<Map<String,Object>> rows=mapper.knowledge(studentId,courseId);
    for(Map<String,Object> r:rows){long n=((Number)r.get("questionCount")).longValue(),c=((Number)r.get("correctCount")).longValue(),people=((Number)r.get("participantCount")).longValue();r.put("accuracy",AnswerRules.accuracy(c,n));r.put("wrongCount",n-c);r.put("level",AnswerRules.level(c,n,studentId!=null||people>=3));}
    List<String> priority=List.of("WEAK","REVIEW","INSUFFICIENT","NO_DATA","GOOD");
    rows.sort(Comparator.<Map<String,Object>>comparingInt(r->priority.indexOf(r.get("level"))).thenComparingDouble(r->r.get("accuracy")==null?101:((Number)r.get("accuracy")).doubleValue()).thenComparing(Comparator.comparingLong((Map<String,Object> r)->((Number)r.get("wrongCount")).longValue()).reversed()));
    return rows;
 }
 @Override public Object trend(long studentId,long courseId){course(courseId);List<Map<String,Object>> rows=mapper.trend(studentId,courseId);Collections.reverse(rows);return rows;}
 @Override public Page<?> wrong(long studentId,Long courseId,Long knowledgeId,int page,int size){int offset=Ids.offset(page,size);List<Map<String,Object>> rows=mapper.wrong(studentId,courseId,knowledgeId,offset,size);for(Map<String,Object> r:rows)r.put("latestCorrect",((Number)r.get("latestCorrect")).intValue()==1);return new Page<>(mapper.wrongCount(studentId,courseId,knowledgeId),rows);}
 @Override public Page<?> courseStudents(long courseId,int page,int size){course(courseId);int offset=Ids.offset(page,size);return new Page<>(users.studentCount(null,null),mapper.courseStudents(courseId,offset,size));}
}

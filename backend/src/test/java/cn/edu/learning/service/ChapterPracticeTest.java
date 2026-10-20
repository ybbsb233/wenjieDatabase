package cn.edu.learning.service;

import cn.edu.learning.exception.ApiException;
import cn.edu.learning.mapper.*;
import cn.edu.learning.pojo.Models.*;
import cn.edu.learning.service.impl.PracticeServiceImpl;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import java.util.*;
import java.util.concurrent.atomic.AtomicLong;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import static org.mockito.ArgumentMatchers.*;

class ChapterPracticeTest {
    @Test void studentsReceiveTheSameTwentyQuestionsAndCanonicalOrder() {
        PracticeMapper practice=mock(PracticeMapper.class);
        QuestionMapper questions=mock(QuestionMapper.class);
        CourseMapper courses=mock(CourseMapper.class);
        when(courses.courses()).thenReturn(List.of(Map.of("id","1")));
        when(courses.chapterMatches(101L,1L)).thenReturn(1);
        List<Question> pool=new ArrayList<>();
        for(long i=1;i<=20;i++)pool.add(new Question(i,101L,1L,"SINGLE","题目"+i,"甲","乙","丙","丁","A","解析"));
        when(questions.candidates(1L,101L,null)).thenReturn(pool);
        AtomicLong nextId=new AtomicLong(1);
        doAnswer(invocation->{Map<String,Object> row=invocation.getArgument(0);row.put("id",nextId.getAndIncrement());return null;}).when(practice).insert(anyMap());
        PracticeServiceImpl service=new PracticeServiceImpl(practice,questions,courses);
        for(long id:List.of(1L,2L))service.startChapter(new User(id,"account","姓名","hash","STUDENT",1,0,0L,null),101L);
        ArgumentCaptor<Long> questionId=ArgumentCaptor.forClass(Long.class);
        ArgumentCaptor<Integer> order=ArgumentCaptor.forClass(Integer.class);
        ArgumentCaptor<String> options=ArgumentCaptor.forClass(String.class);
        verify(practice,times(40)).insertItem(anyLong(),questionId.capture(),order.capture(),options.capture());
        assertEquals(questionId.getAllValues().subList(0,20),questionId.getAllValues().subList(20,40));
        assertEquals(order.getAllValues().subList(0,20),order.getAllValues().subList(20,40));
        for(String permutation:options.getAllValues())assertEquals("ABCD",permutation.chars().sorted().collect(StringBuilder::new,StringBuilder::appendCodePoint,StringBuilder::append).toString());
    }
    @Test void incompleteChapterCannotBeStartedAsFixedSet() {
        PracticeMapper practice=mock(PracticeMapper.class);
        QuestionMapper questions=mock(QuestionMapper.class);
        CourseMapper courses=mock(CourseMapper.class);
        when(courses.courses()).thenReturn(List.of(Map.of("id","1")));
        when(courses.chapterMatches(101L,1L)).thenReturn(1);
        when(questions.candidates(1L,101L,null)).thenReturn(List.of());
        var service=new PracticeServiceImpl(practice,questions,courses);
        var user=new User(1L,"account","姓名","hash","STUDENT",1,0,0L,null);
        assertEquals(409,assertThrows(ApiException.class,()->service.startChapter(user,101L)).status);
        verify(practice,never()).insert(anyMap());
    }
}

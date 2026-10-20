package cn.edu.learning.mapper;
import cn.edu.learning.pojo.Models.*;
import org.apache.ibatis.annotations.Param;
import java.util.*;
public interface PracticeMapper {
 void insert(Map<String,Object> row);
 void insertItem(@Param("practiceId") long practiceId,@Param("questionId") long questionId,@Param("orderNo") int orderNo,@Param("optionOrder") String optionOrder);
 Practice byId(long id);
 Practice lock(long id);
 List<Map<String,Object>> chapterSets(@Param("studentId") long studentId,@Param("courseId") long courseId);
 String chapterTitle(long chapterId);
 List<Item> items(long practiceId);
 void answer(@Param("id") long id,@Param("answer") String answer,@Param("correct") int correct);
 void finish(@Param("id") long id,@Param("correct") int correct);
 List<Map<String,Object>> history(@Param("studentId") long studentId,@Param("courseId") Long courseId,@Param("offset") int offset,@Param("limit") int limit);
 long historyCount(@Param("studentId") long studentId,@Param("courseId") Long courseId);
 List<Map<String,Object>> allHistory(@Param("studentId") Long studentId,@Param("courseId") Long courseId,@Param("offset") int offset,@Param("limit") int limit);
 long allHistoryCount(@Param("studentId") Long studentId,@Param("courseId") Long courseId);
}

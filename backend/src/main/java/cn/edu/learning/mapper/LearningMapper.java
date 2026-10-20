package cn.edu.learning.mapper;
import java.util.*;
import org.apache.ibatis.annotations.Param;
public interface LearningMapper {
 List<Map<String,Object>> summary(@Param("studentId") Long studentId);
 List<Map<String,Object>> knowledge(@Param("studentId") Long studentId,@Param("courseId") long courseId);
 List<Map<String,Object>> trend(@Param("studentId") long studentId,@Param("courseId") long courseId);
 List<Map<String,Object>> wrong(@Param("studentId") long studentId,@Param("courseId") Long courseId,@Param("knowledgeId") Long knowledgeId,@Param("offset") int offset,@Param("limit") int limit);
 long wrongCount(@Param("studentId") long studentId,@Param("courseId") Long courseId,@Param("knowledgeId") Long knowledgeId);
 List<Map<String,Object>> courseStudents(@Param("courseId") long courseId,@Param("offset") int offset,@Param("limit") int limit);
}

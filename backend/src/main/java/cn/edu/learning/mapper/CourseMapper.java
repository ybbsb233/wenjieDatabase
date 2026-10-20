package cn.edu.learning.mapper;
import org.apache.ibatis.annotations.Param;
import java.util.*;
public interface CourseMapper {
    List<Map<String,Object>> courses();
    List<Map<String,Object>> chapters(long courseId);
    List<Map<String,Object>> knowledge(@Param("courseId") long courseId,@Param("chapterId") Long chapterId);
    int courseExists(long id);
    int chapterMatches(@Param("chapterId") long chapterId,@Param("courseId") long courseId);
    int knowledgeMatches(@Param("knowledgeId") long knowledgeId,@Param("courseId") long courseId,@Param("chapterId") Long chapterId);
}

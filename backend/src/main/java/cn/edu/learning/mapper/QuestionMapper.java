package cn.edu.learning.mapper;
import cn.edu.learning.pojo.Models.Question;
import org.apache.ibatis.annotations.Param;
import java.util.List;
public interface QuestionMapper {
 Question byId(long id);
 List<Question> candidates(@Param("courseId") long courseId,@Param("chapterId") Long chapterId,@Param("knowledgeId") Long knowledgeId);
 int wasWrong(@Param("studentId") long studentId,@Param("questionId") long questionId);
}

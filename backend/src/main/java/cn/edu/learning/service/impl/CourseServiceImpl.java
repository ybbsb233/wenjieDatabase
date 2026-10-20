package cn.edu.learning.service.impl;
import cn.edu.learning.exception.ApiException;
import cn.edu.learning.mapper.CourseMapper;
import cn.edu.learning.service.CourseService;
import org.springframework.stereotype.Service;
@Service
public class CourseServiceImpl implements CourseService {
 private final CourseMapper mapper;
 public CourseServiceImpl(CourseMapper mapper){this.mapper=mapper;}
 private void course(long id){if(mapper.courseExists(id)==0)throw new ApiException(404,"课程不存在");}
 @Override public Object courses(){return mapper.courses();}
 @Override public Object chapters(long courseId){course(courseId);return mapper.chapters(courseId);}
 @Override public Object knowledge(long courseId,Long chapterId){course(courseId);if(chapterId!=null&&mapper.chapterMatches(chapterId,courseId)==0)throw new ApiException(400,"章节不属于所选课程");return mapper.knowledge(courseId,chapterId);}
}

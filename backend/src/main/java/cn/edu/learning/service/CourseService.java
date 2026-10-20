package cn.edu.learning.service;
public interface CourseService {
 Object courses();
 Object chapters(long courseId);
 Object knowledge(long courseId,Long chapterId);
}

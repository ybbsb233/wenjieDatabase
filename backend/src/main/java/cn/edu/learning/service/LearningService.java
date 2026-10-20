package cn.edu.learning.service;
import cn.edu.learning.pojo.Models.Page;
import java.util.*;
public interface LearningService {
 Object summary(Long studentId);
 Object knowledge(Long studentId,long courseId);
 Object trend(long studentId,long courseId);
 Page<?> wrong(long studentId,Long courseId,Long knowledgeId,int page,int size);
 Page<?> courseStudents(long courseId,int page,int size);
}

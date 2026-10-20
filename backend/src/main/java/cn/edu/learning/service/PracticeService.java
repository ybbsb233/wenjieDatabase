package cn.edu.learning.service;
import cn.edu.learning.pojo.Models.*;
public interface PracticeService {
 Object start(User user,Start input);
 Object fromWrong(User user,WrongStart input);
 Object chapterSets(User user,long courseId);
 Object startChapter(User user,long chapterId);
 Object questions(User user,long practiceId);
 Object submit(User user,long practiceId,Submit input);
 Object result(User user,long practiceId);
 Page<?> history(long studentId,Long courseId,int page,int size);
 Page<?> allHistory(Long studentId,Long courseId,int page,int size);
}

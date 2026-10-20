package cn.edu.learning.service;
import cn.edu.learning.pojo.Models.*;
public interface StudentService {
 Page<?> list(String keyword,Integer enabled,int page,int size);
 UserView create(NewStudent input);
 UserView student(long id);
 void status(long id,boolean enabled);
 void reset(long id);
 Object counts();
}

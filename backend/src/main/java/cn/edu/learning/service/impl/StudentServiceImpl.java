package cn.edu.learning.service.impl;
import cn.edu.learning.exception.ApiException;
import cn.edu.learning.mapper.UserMapper;
import cn.edu.learning.pojo.Models.*;
import cn.edu.learning.service.StudentService;
import cn.edu.learning.utils.Ids;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import java.util.Map;
@Service
public class StudentServiceImpl implements StudentService {
 private final UserMapper users;private final BCryptPasswordEncoder encoder=new BCryptPasswordEncoder();
 public StudentServiceImpl(UserMapper u){users=u;}
 @Override public Page<?> list(String keyword,Integer enabled,int page,int size){int offset=Ids.offset(page,size);if(enabled!=null&&enabled!=0&&enabled!=1)throw new ApiException(400,"状态不合法");return new Page<>(users.studentCount(keyword,enabled),users.students(keyword,enabled,offset,size).stream().map(UserView::from).toList());}
 @Override public UserView create(NewStudent input){users.insert(input.username(),input.realName().trim(),encoder.encode("123456"),"STUDENT");return UserView.from(users.byUsername(input.username()));}
 private User get(long id){User u=users.byId(id);if(u==null||!u.role().equals("STUDENT"))throw new ApiException(404,"学生不存在");return u;}
 @Override public UserView student(long id){return UserView.from(get(id));}
 @Override public void status(long id,boolean enabled){get(id);users.status(id,enabled?1:0);}
 @Override public void reset(long id){get(id);users.password(id,encoder.encode("123456"),0);}
 @Override public Object counts(){return Map.of("studentCount",users.studentCount(null,null),"enabledCount",users.studentCount(null,1));}
}

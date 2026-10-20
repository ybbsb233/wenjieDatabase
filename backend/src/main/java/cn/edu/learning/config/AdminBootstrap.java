package cn.edu.learning.config;
import cn.edu.learning.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;
@Component
public class AdminBootstrap implements ApplicationRunner {
 private final UserMapper users;private final String initial;
 public AdminBootstrap(UserMapper u,@Value("${app.bootstrap-admin-password:}") String password){users=u;initial=password;}
 @Override public void run(ApplicationArguments args){
    if(users.byUsername("admin")!=null)return;
    if(initial.length()<6||initial.getBytes(java.nio.charset.StandardCharsets.UTF_8).length>72)throw new IllegalStateException("Set ADMIN_INITIAL_PASSWORD (6 to 72 bytes) for first startup");
    users.insert("admin","系统管理员",new BCryptPasswordEncoder().encode(initial),"ADMIN");
 }
}

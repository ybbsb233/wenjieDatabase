package cn.edu.learning.service;
import cn.edu.learning.pojo.Models.*;
public interface AuthService {
    Object login(Login input);
    User verify(String token);
    void password(User user,Password input);
    void logout(User user);
}

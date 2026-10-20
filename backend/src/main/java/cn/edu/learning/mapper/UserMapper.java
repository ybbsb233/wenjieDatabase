package cn.edu.learning.mapper;
import cn.edu.learning.pojo.Models.User;
import org.apache.ibatis.annotations.Param;
import java.util.List;
public interface UserMapper {
    User byUsername(String username);
    User byId(long id);
    int insert(@Param("username") String username,@Param("realName") String realName,@Param("hash") String hash,@Param("role") String role);
    int password(@Param("id") long id,@Param("hash") String hash,@Param("mustChange") int mustChange);
    int revoke(long id);
    int status(@Param("id") long id,@Param("enabled") int enabled);
    List<User> students(@Param("keyword") String keyword,@Param("enabled") Integer enabled,@Param("offset") int offset,@Param("limit") int limit);
    long studentCount(@Param("keyword") String keyword,@Param("enabled") Integer enabled);
}

package cn.edu.learning;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("cn.edu.learning.mapper")
public class LearningApplication {
    public static void main(String[] args) { SpringApplication.run(LearningApplication.class, args); }
}

package cn.edu.learning.service.impl;

import cn.edu.learning.exception.ApiException;
import cn.edu.learning.mapper.UserMapper;
import cn.edu.learning.pojo.Models.*;
import cn.edu.learning.service.AuthService;
import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.Instant;
import java.util.Map;

@Service
public class AuthServiceImpl implements AuthService {
    private final UserMapper users;
    private final Algorithm algorithm;
    private final BCryptPasswordEncoder encoder=new BCryptPasswordEncoder();
    private final String dummy=encoder.encode("not-a-real-password");
    public AuthServiceImpl(UserMapper users,@Value("${app.jwt-secret}") String secret) {
        if(secret.getBytes(java.nio.charset.StandardCharsets.UTF_8).length<32) throw new IllegalArgumentException("JWT_SECRET must contain at least 32 bytes");
        this.users=users; algorithm=Algorithm.HMAC256(secret);
    }
    @Override public Object login(Login input) {
        if(input.password().getBytes(java.nio.charset.StandardCharsets.UTF_8).length>72) throw new ApiException(401,"账号、密码不正确或账号已停用");
        User user=users.byUsername(input.username());
        boolean matches=encoder.matches(input.password(),user==null?dummy:user.passwordHash());
        if(user==null||!matches||user.enabled()!=1) throw new ApiException(401,"账号、密码不正确或账号已停用");
        Instant now=Instant.now();
        String token=JWT.create().withIssuer("learning-analysis").withSubject(user.id().toString()).withClaim("role",user.role()).withClaim("version",user.tokenVersion()).withIssuedAt(now).withExpiresAt(now.plusSeconds(7200)).sign(algorithm);
        return Map.of("token",token,"user",UserView.from(user));
    }
    @Override public User verify(String token) {
        try {
            var jwt=JWT.require(algorithm).withIssuer("learning-analysis").build().verify(token);
            if(jwt.getExpiresAt()==null) throw new IllegalArgumentException();
            User user=users.byId(Long.parseLong(jwt.getSubject()));
            if(user==null||user.enabled()!=1||!user.tokenVersion().equals(jwt.getClaim("version").asLong())||!user.role().equals(jwt.getClaim("role").asString())) throw new IllegalArgumentException();
            return user;
        } catch(com.auth0.jwt.exceptions.JWTVerificationException|IllegalArgumentException e) { throw new ApiException(401,"登录已失效，请重新登录"); }
    }
    @Transactional @Override public void password(User user,Password input) {
        if(input.newPassword().equals("123456")||input.newPassword().getBytes(java.nio.charset.StandardCharsets.UTF_8).length>72) throw new ApiException(400,"新密码不能为默认密码且不能超过72字节");
        User current=users.byId(user.id());
        if(!encoder.matches(input.oldPassword(),current.passwordHash())) throw new ApiException(400,"原密码不正确");
        users.password(user.id(),encoder.encode(input.newPassword()),0);
    }
    @Override public void logout(User user) { users.revoke(user.id()); }
}

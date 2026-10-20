package cn.edu.learning.controller;
import cn.edu.learning.pojo.Models.*;
import cn.edu.learning.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/api/auth")
public class AuthController {
    private final AuthService auth;
    public AuthController(AuthService auth) { this.auth=auth; }
    @PostMapping("/login") public Result login(@Valid @RequestBody Login input) { return Result.ok(auth.login(input)); }
    @GetMapping("/me") public Result me(@RequestAttribute("currentUser") User user) { return Result.ok(UserView.from(user)); }
    @PostMapping("/logout") public Result logout(@RequestAttribute("currentUser") User user) { auth.logout(user); return Result.ok(null); }
    @PutMapping("/password") public Result password(@RequestAttribute("currentUser") User user,@Valid @RequestBody Password input) { auth.password(user,input); return Result.ok(null); }
}

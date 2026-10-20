package cn.edu.learning.controller;
import cn.edu.learning.pojo.Models.*;
import cn.edu.learning.service.StudentService;
import cn.edu.learning.utils.Ids;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/api/admin/students")
public class AdminStudentController {
 private final StudentService service;
 public AdminStudentController(StudentService s){service=s;}
 @GetMapping public Result list(@RequestParam(required=false) String keyword,@RequestParam(required=false) Integer enabled,@RequestParam(defaultValue="1") int page,@RequestParam(defaultValue="10") int pageSize){return Result.ok(service.list(keyword,enabled,page,pageSize));}
 @PostMapping public Result create(@Valid @RequestBody NewStudent input){return Result.ok(service.create(input));}
 @GetMapping("/{id}") public Result get(@PathVariable String id){return Result.ok(service.student(Ids.parse(id)));}
 @PutMapping("/{id}/status") public Result status(@PathVariable String id,@Valid @RequestBody Status input){service.status(Ids.parse(id),input.enabled());return Result.ok(null);}
 @PostMapping("/{id}/reset-password") public Result reset(@PathVariable String id){service.reset(Ids.parse(id));return Result.ok(null);}
}

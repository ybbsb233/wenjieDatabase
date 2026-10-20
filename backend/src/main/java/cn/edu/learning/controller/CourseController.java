package cn.edu.learning.controller;
import cn.edu.learning.service.CourseService;
import cn.edu.learning.pojo.Models.Result;
import cn.edu.learning.exception.ApiException;
import cn.edu.learning.utils.Ids;
import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/api/courses")
public class CourseController {
 private final CourseService service;
 public CourseController(CourseService service){this.service=service;}
 @GetMapping public Result courses(){return Result.ok(service.courses());}
 @GetMapping("/{id}/chapters") public Result chapters(@PathVariable String id){return Result.ok(service.chapters(Ids.parse(id)));}
 @GetMapping("/{id}/knowledge-points") public Result knowledge(@PathVariable String id,@RequestParam(required=false) String chapterId){return Result.ok(service.knowledge(Ids.parse(id),Ids.optional(chapterId)));}
}

package cn.edu.learning.controller;
import cn.edu.learning.pojo.Models.*;
import cn.edu.learning.service.LearningService;
import cn.edu.learning.utils.Ids;
import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/api/student")
public class LearningController {
 private final LearningService service;
 public LearningController(LearningService s){service=s;}
 @GetMapping("/summary") public Result summary(@RequestAttribute("currentUser") User u){return Result.ok(service.summary(u.id()));}
 @GetMapping("/knowledge-analysis") public Result analysis(@RequestAttribute("currentUser") User u,@RequestParam String courseId){return Result.ok(service.knowledge(u.id(),Ids.parse(courseId)));}
 @GetMapping("/trend") public Result trend(@RequestAttribute("currentUser") User u,@RequestParam String courseId){return Result.ok(service.trend(u.id(),Ids.parse(courseId)));}
 @GetMapping("/wrong-questions") public Result wrong(@RequestAttribute("currentUser") User u,@RequestParam(required=false) String courseId,@RequestParam(required=false) String knowledgeId,@RequestParam(defaultValue="1") int page,@RequestParam(defaultValue="10") int pageSize){return Result.ok(service.wrong(u.id(),Ids.optional(courseId),Ids.optional(knowledgeId),page,pageSize));}
}

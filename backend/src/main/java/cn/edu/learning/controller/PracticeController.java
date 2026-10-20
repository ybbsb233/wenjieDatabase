package cn.edu.learning.controller;
import cn.edu.learning.pojo.Models.*;
import cn.edu.learning.service.PracticeService;
import cn.edu.learning.utils.Ids;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/api/student/practices")
public class PracticeController {
 private final PracticeService service;
 public PracticeController(PracticeService service){this.service=service;}
 @PostMapping public Result start(@RequestAttribute("currentUser") User u,@Valid @RequestBody Start body){return Result.ok(service.start(u,body));}
 @PostMapping("/from-wrong") public Result wrong(@RequestAttribute("currentUser") User u,@Valid @RequestBody WrongStart body){return Result.ok(service.fromWrong(u,body));}
 @GetMapping("/chapter-sets") public Result chapterSets(@RequestAttribute("currentUser") User u,@RequestParam String courseId){return Result.ok(service.chapterSets(u,Ids.parse(courseId)));}
 @PostMapping("/chapters/{id}") public Result chapter(@RequestAttribute("currentUser") User u,@PathVariable String id){return Result.ok(service.startChapter(u,Ids.parse(id)));}
 @GetMapping("/{id}/questions") public Result questions(@RequestAttribute("currentUser") User u,@PathVariable String id){return Result.ok(service.questions(u,Ids.parse(id)));}
 @PostMapping("/{id}/submit") public Result submit(@RequestAttribute("currentUser") User u,@PathVariable String id,@Valid @RequestBody Submit body){return Result.ok(service.submit(u,Ids.parse(id),body));}
 @GetMapping("/{id}/result") public Result result(@RequestAttribute("currentUser") User u,@PathVariable String id){return Result.ok(service.result(u,Ids.parse(id)));}
 @GetMapping public Result history(@RequestAttribute("currentUser") User u,@RequestParam(required=false) String courseId,@RequestParam(defaultValue="1") int page,@RequestParam(defaultValue="10") int pageSize){return Result.ok(service.history(u.id(),Ids.optional(courseId),page,pageSize));}
}

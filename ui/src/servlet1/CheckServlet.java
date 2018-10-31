package servlet1;

import java.io.IOException; 
import java.io.PrintWriter; 
  
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet; 
import javax.servlet.http.HttpServletRequest; 
import javax.servlet.http.HttpServletResponse; 
@WebServlet("/CheckServlet")
public class CheckServlet extends HttpServlet { 
  
  public void doGet(HttpServletRequest request, HttpServletResponse response) 
      throws ServletException, IOException { 
    doPost(request, response); 
  } 
  
  public void doPost(HttpServletRequest request, HttpServletResponse response) 
      throws ServletException, IOException { 
    /*设置字符集为'UTF-8'*/
    request.setCharacterEncoding("UTF-8"); 
    response.setCharacterEncoding("UTF-8"); 
    String userid = request.getParameter("userid"); // 接收userid 
    String sex = request.getParameter("sex");//接收性别 
    System.out.println(userid); 
    System.out.println(sex); 
    System.out.println("ok");
    PrintWriter pw = response.getWriter(); 
    String json = "{'success':'nn','false':'yy'}"; 
    pw.print(json); 
    pw.flush(); 
    pw.close(); 
    
    
  
    //写返回的JSON 
   
    
  
  } 
} 

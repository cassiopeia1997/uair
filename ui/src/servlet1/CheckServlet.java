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
    /*�����ַ���Ϊ'UTF-8'*/
    request.setCharacterEncoding("UTF-8"); 
    response.setCharacterEncoding("UTF-8"); 
    String userid = request.getParameter("userid"); // ����userid 
    String sex = request.getParameter("sex");//�����Ա� 
    System.out.println(userid); 
    System.out.println(sex); 
    System.out.println("ok");
    PrintWriter pw = response.getWriter(); 
    String json = "{'success':'nn','false':'yy'}"; 
    pw.print(json); 
    pw.flush(); 
    pw.close(); 
    
    
  
    //д���ص�JSON 
   
    
  
  } 
} 

package servlet1;

import java.sql.*;
import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedReader;  
import java.io.File;  
import java.io.FileInputStream;  
import java.io.FileReader;  
import java.io.IOException;  
import java.io.InputStream;  
import java.io.InputStreamReader;  
import java.io.RandomAccessFile;  
import java.io.Reader;  

import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;
import java.io.*;
import java.io.IOException;
/**
 * Servlet implementation class second
 */
@WebServlet("/second")
public class second extends HttpServlet {
	private static final long serialVersionUID = 1L;
	static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";  
    static final String DB_URL = "jdbc:mysql://localhost:3306/test";
    
    // 数据库的用户名与密码，需要根据自己的设置
    static final String USER = "root";
    static final String PASS = "121502";
    /**
     * @see HttpServlet#HttpServlet()
     */
    public second() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		 
	    Connection conn = null;
        Statement stmt = null;
        PrintWriter out=response.getWriter();
	    Double sw_lng = Double.parseDouble(request.getParameter("sw_lng")); 
	    Double sw_lat = Double.parseDouble(request.getParameter("sw_lat"));
	    Double ne_lng = Double.parseDouble(request.getParameter("ne_lng")); 
	    Double ne_lat = Double.parseDouble(request.getParameter("ne_lat"));
	    String pm10= null;
	    JSONArray returnjson = new JSONArray();
	    try{
	    	Class.forName("com.mysql.jdbc.Driver");
            
            // 打开一个连接
            conn = DriverManager.getConnection(DB_URL,USER,PASS);

            // 执行 SQL 查询
            stmt = conn.createStatement();
            String sql;
            sql = "SELECT * from grid where max_lat<"+ne_lat+"and min_lat>"+sw_lat+"and max_lng<"+ne_lng+"and min_lng>"+sw_lng;
            ResultSet rs = stmt.executeQuery(sql);
            while(rs.next()){
            	if(rs.getString("pm10").equals("None")){pm10="None";}
            	else{
            	int pm10temp=Integer.parseInt(rs.getString("pm10"));
     			if (pm10temp<=50){pm10="G";}
     			else{if (pm10temp<=100)
     					{pm10="M";}
     				else{
     					if (pm10temp<=150){pm10="U-S";}
     					else{
     						if (pm10temp<=200){pm10="U";}
     						else{
     							if (pm10temp<=300){pm10="VU";}
     							else{pm10="H";
     							}
     						}
     					}
     					}
     			}
            	}
            	JSONObject ls1=new JSONObject();
		        try {
		            //第一个name和sex
		            ls1.put("max_lng",rs.getString("max_lng"));
		            ls1.put("max_lat",rs.getString("max_lat"));
		            ls1.put("min_lng",rs.getString("min_lng"));
		            ls1.put("min_lat",rs.getString("min_lat"));
		            ls1.put("PM10",pm10);
		            //System.out.println(ls1);
		           returnjson.put(ls1);
		           
		            //添加到json中
		    
		        } catch (JSONException e) {
		            // TODO Auto-generated catch block
		            e.printStackTrace();
		        }
            }

	    }
	    catch(SQLException se) {
            // 处理 JDBC 错误
            se.printStackTrace();
        } catch(Exception e) {
            // 处理 Class.forName 错误
            e.printStackTrace();
        }finally{
            // 最后是用于关闭资源的块
            try{
                if(stmt!=null)
                stmt.close();
            }catch(SQLException se2){
            }
            try{
                if(conn!=null)
                conn.close();
            }catch(SQLException se){
                se.printStackTrace();
            }
        }

	    /*
	    String txt1= "C:\\Users\\cassiopeia\\Desktop\\uair\\code\\ui\\src\\servlet1\\grid.txt";
	    String txt2="C:\\Users\\cassiopeia\\Desktop\\uair\\code\\ui\\src\\servlet1\\aqi_0226_1630.txt";
	    File file1 =new File(txt1);
	    File file2 =new File(txt2);
	    BufferedReader reader1=null;
	    BufferedReader reader2=null;
	    String line1=null;
	    String line2=null;
	    String lineuse=null;
	    JSONArray returnjson = new JSONArray();
	    int i=0;
	   
		try{
		reader1=new BufferedReader(new FileReader(file1));
		reader2=new BufferedReader(new FileReader(file2));
		while ((line1 = reader1.readLine()) != null){
			
			line2=reader2.readLine();
			String[] info=line1.split(" ");
			
			if(Double.parseDouble(info[0])<=ne_lat && Double.parseDouble(info[1])>=sw_lat){
				if(Double.parseDouble(info[2])<=ne_lng && Double.parseDouble(info[3])>=sw_lng){
					lineuse=line2;
					String pm10=null;
					//System.out.println("ok");
					if (lineuse!=null){
						
						String[] infos=lineuse.split(" ");
						for(int j=0;j<infos.length-1;j++){ 
							
							if (j==1){continue;}
							String[] details=infos[j].split("\\_");
							
							if(details[0].equals("PM10")){
								if(details[1].equals("None")){
									continue;
								}
								int pm10temp=Integer.parseInt(details[1]);
								if (pm10temp<=50){pm10="G";}
								else{if (pm10temp<=100)
										{pm10="M";}
									else{
										if (pm10temp<=150){pm10="U-S";}
										else{
											if (pm10temp<=200){pm10="U";}
											else{
												if (pm10temp<=300){pm10="VU";}
												else{pm10="H";
												}
											}
										}
										}
									}
								
								
							}
							
						}
					JSONObject ls1=new JSONObject();
			        try {
			            //第一个name和sex
			            ls1.put("max_lng", info[2]);
			            ls1.put("max_lat",info[0]);
			            ls1.put("min_lng",info[3]);
			            ls1.put("min_lat",info[1]);
			            ls1.put("PM10",pm10);
			            //System.out.println(ls1);
			           returnjson.put(ls1);
			            i++;
			            //添加到json中
			    
			        } catch (JSONException e) {
			            // TODO Auto-generated catch block
			            e.printStackTrace();
			        }
				}
			}
		}
		}
		}
		catch(IOException e){
			e.printStackTrace();}*/
		JSONObject allpm10=new JSONObject();
		try{
			allpm10.put("allgrids",returnjson);
			//System.out.println(allpm10);
			//System.out.println(i);
			out.print(allpm10.toString());
		}catch(JSONException e){
			e.printStackTrace();
		}
		
		
		}
		/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}

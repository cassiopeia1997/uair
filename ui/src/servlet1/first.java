package servlet1;



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
import java.io.*;
import java.io.IOException;
import java.sql.*;

/**
 * Servlet implementation class first
 */
@WebServlet("/first")
public class first extends HttpServlet {
	private static final long serialVersionUID = 1L;
    // JDBC �����������ݿ� URL
    static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";  
    static final String DB_URL = "jdbc:mysql://localhost:3306/test";
    
    // ���ݿ���û��������룬��Ҫ�����Լ�������
    static final String USER = "root";
    static final String PASS = "121502"; 

    /**
     * @see HttpServlet#HttpServlet()
     */
    public first() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		 doPost(request, response); 
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		Connection conn = null;
        Statement stmt = null;
		PrintWriter out=response.getWriter();
	    String lng = request.getParameter("lng"); // ����userid 
	    String lat = request.getParameter("lat");//�����Ա� 
	    System.out.println(lng); 
	    System.out.println(lat); 
	    String temperature="null";
		String humidity="null";
		String wind="null";
		String pressure="null";
		String pm10="null";
	    try{
	    Class.forName("com.mysql.jdbc.Driver");
        
        // ��һ������
        conn = DriverManager.getConnection(DB_URL,USER,PASS);

        // ִ�� SQL ��ѯ
        stmt = conn.createStatement();
        String sql;
        sql = "SELECT * FROM aqi where id=ANY( select id from grid where max_lat>"+lat+"and min_lat<"+lat +"and max_lng>"+lng +"and min_lng<"+lng+")";
        ResultSet rs = stmt.executeQuery(sql);
        while (rs.next()){
        	int id  = rs.getInt("id");
            temperature= rs.getString("temperature");
            humidity = rs.getString("humidity");
            wind = rs.getString("wind");
            pressure = rs.getString("pressure");
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
            // �������
           // System.out.println(pm10);

        }
        rs.close();
        stmt.close();
        conn.close();
        }
	    catch(SQLException se) {
            // ���� JDBC ����
            se.printStackTrace();
        } catch(Exception e) {
            // ���� Class.forName ����
            e.printStackTrace();
        }finally{
            // ��������ڹر���Դ�Ŀ�
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
	    int linenum=0;
	    linenum=readFileByLines("C:\\Users\\cassiopeia\\Desktop\\uair\\code\\ui\\src\\servlet1\\grid.txt",lng,lat);
	    
	    String info=searchInfo(linenum,"C:\\Users\\cassiopeia\\Desktop\\uair\\code\\ui\\src\\servlet1\\aqi_0226_1630.txt");
	    
		
		String temperature="null";
		String humidity="null";
		String wind="null";
		String pressure="null";
		String pm10="null";
		if (info!=null){
		
		String[] infos=info.split(" ");
		for(int j=0;j<infos.length-1;j++){ 
			
			if (j==1){continue;}
			String[] details=infos[j].split("\\_");
			
			if (details[0].equals("Temperature")){
				temperature=details[1];
			}
			if (details[0].equals("Humidity")){
				 humidity=details[1];
			}
			if (details[0].equals("Wind")){
				wind=details[1];
			}
			if (details[0].equals("Pressure")){
				pressure=details[1];
			}
			if(details[0].equals("PM10")){
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
		System.out.println(info);}
		//String all="{'Temperature':tempereature,'Humidity':humidity,'Wind':wind,'Pressure':pressure}";
       */
       JSONObject ls1=new JSONObject();
   

        try {
            //��һ��name��sex
            ls1.put("Temperature", temperature);
            ls1.put("Pressure",pressure);
            ls1.put("Humidity",humidity);
            ls1.put("Wind",wind);
            ls1.put("PM10",pm10);
            
            //��ӵ�json��
    
        } catch (JSONException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        //System.out.println(ls1);  
        try{
	    System.out.println(ls1.getString("Temperature"));}
        catch(JSONException e){e.printStackTrace();  }
        
	    out.write(ls1.toString());
	    out.flush();
	    out.close();
	    
	    
	}
	
	public String searchInfo(int linenum, String fileName){
		String info=null;
		File file =new File(fileName);
		//System.out.println(linenum);
		BufferedReader reader=null;
		try{
		reader=new BufferedReader(new FileReader(file));
		int countnum=0;
		String line=null;
		while (countnum<=linenum){
			line=reader.readLine();
			countnum++;
		}
		info=line;
		reader.close();
		}
		catch (IOException e) {  
	          e.printStackTrace();  
	       }
		return info;
		
	}
	public int readFileByLines (String fileName, String lng, String lat){
		File file =new File(fileName);
		BufferedReader reader=null;
		int check=0;
		int linenum=-1;
		int line=-1;
		try{
			reader=new BufferedReader(new FileReader(file));
			String tempString=null;
			while(check==0){
			
			linenum=linenum+1;
			tempString=reader.readLine();
			if (tempString==null){break;}
			String[] info=tempString.split(" ");
			//System.out.print(tempString);
			//System.out.print(Double.parseDouble(lat));
			//System.out.println(Double.parseDouble(info[0]));
			if( Double.parseDouble(info[0])>=Double.parseDouble(lat)){
				if (Double.parseDouble(info[1])<=Double.parseDouble(lat)){
					if (Double.parseDouble(info[2])>=Double.parseDouble(lng)){
						if (Double.parseDouble(info[3])<=Double.parseDouble(lng)){
							line=linenum;
							break;
						}
						else{continue;}
					}
					else{continue;}
				}
				else{continue;}
			}
			else{continue;}
			
			
			}
			//add choose line
			reader.close();

		}
		catch (IOException e) {  
			          e.printStackTrace();  
			       }
		return line; 
		
		
		
	}

}

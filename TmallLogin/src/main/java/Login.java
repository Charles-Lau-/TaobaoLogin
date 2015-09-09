/**
 * Created by Pengkun on 2015/9/7.
 * 程序的使用方式如下
 *           Login lo = new Login()
 *           lo.login()
 *           到此时则登录完毕
 *           调用 getCookies 方法来获取登录后得到的cookie 以备后用，值是一个header 列表
 *           lo.getCookies()
 *
 *程序的输入如下:
 *           headers.json
 *           params.json
 *           两个分别是包含请求头 和 请求参数的json文件
 *           在params.json中的  TPL_password2 ， ua 以及 TPL_username 是可变的
 *           其中TPL_password2 和 UA 需要根据用户名去浏览器中抓取
 *注意：
 *           目前对于验证码的处理是手动输入处理
 */

import com.google.gson.Gson;
import org.apache.http.Header;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.apache.http.impl.client.HttpClients.createDefault;

public class Login {
    private String Jtoken = "";
    private String st = "";
    private Map<String,String> loginParams = new HashMap<String,String>();
    private Map<String,String> loginHeaders = new HashMap<String,String>();
    private HttpClient  client = createDefault();
    private Header[] cookie = null;

    //通过json文件，将http请求头和参数读取进来
    public Login(){
         this.loginParams = Login.getParams();
         this.loginHeaders = Login.getHeaders();
    }


    //进行第一次登录请求，并判断是否被要求提交验证码
    public HttpResponse firstLogin()    {
        String url = "https://login.taobao.com/member/login.jhtml";
        HttpPost httpPost = new HttpPost(url);
        //设置请求头ͷ
        for(Map.Entry<String,String> pairEntry: this.loginHeaders.entrySet())
            httpPost.addHeader(pairEntry.getKey(),pairEntry.getValue());
        //设置请求参数
        List<NameValuePair> postParams = new ArrayList<NameValuePair>();
        for(Map.Entry<String,String> pairEntry: this.loginParams.entrySet()){
            postParams.add(new BasicNameValuePair(pairEntry.getKey(), pairEntry.getValue()));
        }
        HttpResponse httpResponse = null;
        //提交请求
        try {
            httpPost.setEntity(new UrlEncodedFormEntity(postParams));
            httpResponse = this.client.execute(httpPost);


        }
        catch(UnsupportedEncodingException e){
            e.printStackTrace();
        }
        catch(IOException e){
            e.printStackTrace();
        }

        return httpResponse;
    }


    //查看是否需要提交验证码
    private boolean  needCheckcode(String content){
        return content.contains("data-src=\"https://pin.aliyun.com");
    }


    //根据验证码 再次提交登录请求
    private HttpResponse loginWithCheckcode(String checkCode){
        this.loginParams.put("TPL_checkcode",checkCode);
        return this.firstLogin();
    }


    //从response object里面提取回复的文本，即网页源代码
    public static String getContent(HttpResponse response){
        String response_content = null;
        try {
            response_content = EntityUtils.toString(response.getEntity());
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(-1);
        }
        return response_content;
    }


    //提取验证码链接，并通过手动输入验证码来获取值
    private String getCheckCode(String content){
        String checkCodeUrl = null;
        Pattern checkcodePattern = Pattern.compile("data-src=\"(.*?)\"");
        Matcher m = checkcodePattern.matcher(content);
        while(m.find())
            checkCodeUrl = m.group(1);

        Scanner sc = new Scanner(System.in);
        System.out.println(checkCodeUrl);
        System.out.println("Please enter checkcode:");
        return  sc.next();

    }


    //登录成功后，从返回的文本里面提取 JToken
    private void setJtoken(String content){
        String Jtoken = null;
        Pattern jtokenPattern = Pattern.compile("id=\"J_HToken\" value=\"(.*?)\"");
        Matcher m = jtokenPattern.matcher(content);
        if(m.find())
            Jtoken  = m.group(1);
        if(Jtoken==null)
        {
            System.out.println("checkcode is wrong, can not get JToken");
            System.exit(-1);
        }
        this.Jtoken = Jtoken;
    }


    //根据Jtoken 来提取 ST， ST码是最终用于登录的值
    private void setSt(){
        String tokenURL = "https://passport.alipay.com/mini_apply_st.js?site=0&token="+this.Jtoken+"&callback=stCallback6";
        HttpClient  client = createDefault();
        HttpGet   getSt = new HttpGet(tokenURL);
        HttpResponse response = null;
        try {
            response = client.execute(getSt);
        } catch (IOException e) {
            e.printStackTrace();
        }
        String content = Login.getContent(response);
        Pattern stPattern = Pattern.compile(".\"st\":\"(.*?)\".");
        Matcher m = stPattern.matcher(content);
        String stCode = null;
        if(m.find())
            stCode = m.group(1);

        if(stCode == null){
            System.out.println("Getting st code is failed");
            System.exit(-1);
        }
        this.st = stCode;

    }


    //根据获得的ST，来进行最终登录，获得后续操作需要的cookie
    private void loginWithSt(){
        String url  = "https://login.taobao.com/member/vst.htm?st="+this.st+"&TPL_username="+this.loginParams.get("TPL_username");
        HttpClient client = createDefault();
        HttpGet httpget = new HttpGet(url);
        HttpResponse response = null;
        try {
            response = client.execute(httpget);
        } catch (IOException e) {
            e.printStackTrace();
        }
        String content = Login.getContent(response);
        if(this.loginSuccessfully(content)) {
            this.cookie = response.getHeaders("Set-Cookie");
            System.out.println("login successfully");
        }
        else
        {
            System.out.println("login failed");
            System.exit(-1);
        }
    }


    //检查是否最终登录成功
    private boolean loginSuccessfully(String content){
        Pattern  p = Pattern.compile("top.location = \"(.*?)\"");
        Matcher m  = p.matcher(content);
        if(m.find())
            return true;
        else
            return false;
    }


    //主程序入口
    public void login(){
        HttpResponse firstResponse = this.firstLogin();
        String firstContent = Login.getContent(firstResponse);
        if(this.needCheckcode(firstContent)){
            String checkCode= this.getCheckCode(firstContent);
            firstResponse = this.loginWithCheckcode(checkCode);
            firstContent = Login.getContent(firstResponse);
        }

        this.setJtoken(firstContent);
        this.setSt();
        this.loginWithSt();
    }

    //返回最终的的cookie
    public Header[] getCookie(){
          return this.cookie;
    }

    //json文件读取函数
    public static Map<String,String> getHeaders(){
        String header_path = System.getProperty("user.dir")+"\\src\\main\\resources\\headers.json";
        return Login.fileToMap(header_path);
    }
    public static Map<String,String> getParams(){
        String params_path = System.getProperty("user.dir")+"\\src\\main\\resources\\params.json";
        return Login.fileToMap(params_path);
    }
    private static Map<String,String> fileToMap(String path){
        BufferedReader reader = null;
        String jsonStr = "";
        String s = "";
        try {
            reader = new BufferedReader(new FileReader(path));
            while((s=reader.readLine())!= null)
                jsonStr += s;
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e){
            e.printStackTrace();
        }

        Map<String,String> mapObj = new Gson().fromJson(jsonStr,HashMap.class);

        return mapObj;
    }


}

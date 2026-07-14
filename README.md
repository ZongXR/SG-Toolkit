<h1>SG-Toolkit</h1>
<p>使用科技手段对抗形式主义，提供了一些自动化脚本。能够帮助你完成网上学堂刷课、安全知识考试自动答题，等</p>
<h2>怎么用？</h2>
<h3>网上学堂刷课</h3>
<pre>
browser = FuckGWXT(
    "san.zhang",
    "1q2w!Q@W",
    "美国能源",
    "http://localhost/www/command/CollegeControl?flag=collegeTC&tcID=ef8afbf81de&tab=collTcLesson&type=&worktypeid=&pageNo1=15&pageSize1=10&comewho=null"
)
browser.process()
</pre>
<h3>安全知识答题</h3>
<h4>代码示例</h4>
<pre>
browser = FuckAnGui(
    "san.zhang",
    "1qaz@WSX",
    "http://localhost/comlogin/routeLogin.html",
    "./题库.xlsx"
)
browser.process()
</pre>
<h4>题库格式</h4>
<table>
<tr>
<th>题型</th><th>题干</th><th>选项</th><th>答案</th>
</tr>
<tr>
<td>单选题</td><td>你今天吃的什么早点？</td><td>A-豆浆|B-八宝粥|C-胡辣汤|D-肉夹馍</td><td>A</td>
</tr>
<tr>
<td>多选题</td><td>你今天吃的什么早点？</td><td>A-豆浆|B-八宝粥|C-胡辣汤|D-肉夹馍</td><td>BCD</td>
</tr>
<tr>
<td>判断题</td><td>今天的早点有豆浆</td><td>A-正确|B-错误</td><td>A</td>
</tr>
</table>
<h4>注意事项</h4>
<p>第一次运行程序必定失败，在弹出的窗口输入用户名、密码、验证码，点击登录，浏览器将自动保存登录信息。下次运行即可自动答题。</p>
<h2>环境要求</h2>
<ul>
<li>Chrome浏览器</li>
<li>Chrome WebDriver（版本需与浏览器保持一致）</li>
<li>Python</li>
<li>Python第三方库（见<a href="requirements.txt" target="_blank">requirements.txt</a>）</li>
</ul>
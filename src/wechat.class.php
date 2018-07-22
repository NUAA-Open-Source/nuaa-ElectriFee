<?php
class WeChat {
	private $callback_function = null;
	private $articles = array();

	public $fromUser = null;
	public $toUser = null;

	//构造函数， 返回WeChat实例
	function __construct($callback_function) {
		$this->callback_function = $callback_function;
	}

	//解析微信post过来的数据
	public function process() {
		if (empty($postData = file_get_contents('php://input'))) return;
		$object = simplexml_load_string($postData, 'SimpleXMLElement', LIBXML_NOCDATA);
		$messgeType = $object->MsgType;
		$this->fromUser = $object->FromUserName;
		$this->toUser = $object->ToUserName;
		switch($messgeType){
			case "text":
				call_user_func($this->callback_function, $this, "text", $object->Content, "", "");
				break;
			case "event":
				switch ($object->Event)
				{
					case "subscribe":	call_user_func($this->callback_function, $this, "subscribe", $object->FromUserName, "", "");    break;
					case "unsubscribe":    call_user_func($this->callback_function, $this, "unsubscribe", $object->FromUserName, "", "");    break;
					case "CLICK":    call_user_func($this->callback_function, $this, "click", $object->EventKey, "", "");    break;
				}
				break;
		}
	}

	//响应文本消息的方法
	protected function textResponse($toUser, $fromUser, $content){
		$xmlTemplate = "<xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    </xml>";
		$xmlText = sprintf($xmlTemplate, $toUser, $fromUser, time(), $content);
		return $xmlText;
	}

	public function sendText($content){
		echo $this->textResponse($this->fromUser, $this->toUser, $content);
	}

	//响应图文消息的方法
	protected function newsResponse($toUser, $fromUser, $articles){
		$xmlTemplate = "<xml>
					<ToUserName><![CDATA[%s]]></ToUserName>
					<FromUserName><![CDATA[%s]]></FromUserName>
					<CreateTime>%s</CreateTime>
					<MsgType><![CDATA[news]]></MsgType>
					";
		$xmlText = sprintf($xmlTemplate, $toUser, $fromUser, time());
		$xmlText .= '<ArticleCount>'. count($articles) .'</ArticleCount>';
		$xmlText .= '<Articles>';
		foreach($articles as  $article) {
			$xmlText .= '<item>';
			$xmlText .= '<Title><![CDATA[' . $article['Title'] . ']]></Title>';
			$xmlText .= '<Description><![CDATA[' . $article['Description'] . ']]></Description>';
			$xmlText .= '<PicUrl><![CDATA[' . $article['PicUrl'] . ']]></PicUrl>';
			$xmlText .= '<Url><![CDATA[' . $article['Url'] . ']]></Url>';
			$xmlText .= '</item>';
		}
		$xmlText .= '</Articles> </xml>';
		return $xmlText;
	}
	public function addNews($title, $description, $url, $pictureUrl){
		$article = array('Title' => $title,
				'Description' => $description,
				'PicUrl' => $pictureUrl,
				'Url'=>$url);
		$this->articles[] = $article;
	}
	public function sendNews(){
		echo $this->newsResponse($this->fromUser, $this->toUser, $this->articles);
	}
}
?>

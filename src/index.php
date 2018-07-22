<?php
require 'wechat.class.php';

$object = new WeChat("onMessage");
$object->process();

function onMessage(WeChat $object, $messageType, $content, $arg1, $arg2)
{
        switch($messageType){
                case 'text':
                        if (strlen($content) === 8 and substr($content, 0, 1)==='2' and substr($content, 1, 1)==='1')
                        {
                                exec("python main.py $content", $output, $ret_code);
                                $object->sendText("剩余电费（可能存在延迟）：\n".$output[0]);
                        }
                        else $object->sendText("您好，输入错误，本公众号暂时只支持21栋空调电费查询。\n查询格式：楼栋+大寝号+小寝号\n例如：您住在21栋60305，请输入：21060305\n低于10层的不要忘记加0哦！\n提醒：由于个人能力有限，暂时不支持15层及18层、19层的电费查询，查询将会出现错误");
                break;
                case 'subscribe':
                        $object->sendText("您好，欢迎关注裂帛碎玉的想法。本公众号文章从个人博客 vvzero.com 搬迁\n本公众号的扩展功能：\n支持南京航空航天大学将军路校区21栋空调电费查询。\n查询格式：楼栋+大寝号+小寝号\n例如：您住在21栋60305，请输入：21060305\n低于10层的不要忘记加0哦！\n提醒：由于个人能力有限，暂时不支持15层及18层、19层的电费查询，查询将会出现错误");
                break;
        }
                
}
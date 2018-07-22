<?php
require 'wechat.class.php';

$object = new WeChat("onMessage");
$object->process();

function onMessage(WeChat $object, $messageType, $content, $arg1, $arg2)
{
        if ($content=='苏瑞辅') $object->sendText("傻逼一个");
        elseif( $content=="冯锦瑾") $object->sendText("天下无敌");
}
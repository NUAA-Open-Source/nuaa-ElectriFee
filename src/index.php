<?php
require 'wechat.class.php';

$object = new WeChat("onMessage");
$object->process();

function onMessage(WeChat $object, $messageType, $content, $arg1, $arg2)
{
        exec("python main.py $content", $output, $ret_code);
        $object->sendText($output[0]);
}
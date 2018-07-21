<?php
require 'Wechat.class.php';

$object = new WeChat("onMessage");
$object->process();

function onMessage(WeChat $object, $messageType, $content, $arg1, $arg2)
{
    switch ($messageType) {
            case "subscribe":
                   
                break;
            case "text":
                if( ) {

                }
                break;
            case "click":
                if( ) {

                }
        }
}

<?php
exec('python3 1.py', $output, $ret_code);
echo $output[0];

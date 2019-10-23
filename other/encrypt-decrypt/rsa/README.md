## 生成私钥、公钥
    $ openssl genrsa -out private_key.pem 1024 # 生成指定1024位的私钥
    $ openssl rsa -in private_key.pem -pubout -out public_key.pem # 由私钥转出公钥
    
## 转换
    DER和PEM是X509和其他证书中使用的格式，用于存储公钥，私钥和其他相关信息
    
    说明:
        inform：表示输入格式
        outform：表示输出格式
        in：表示输入文件
        out：表示输出文件

----------
    RSA密钥格式转化
    PEM转DER
    $ openssl rsa -inform PEM -outform DER -text -in mykey.pem -out mykey.der
    
    DER转PEM
    $ openssl rsa -inform DER -outform PEM -in mykey.der -out mykey.pem

----------
    X509格式转化
    PEM转DER
    $ openssl x509 -inform PEM -outform DER -text -in mykey.pem -out mykey.der
    
    DER转PEM
    $ openssl x509 -inform DER -outform PEM -text -in mykey.der -out mykey.pem

## Python代码
```python
# pip3 install pycryptodome==3.6.4

import io
import binascii
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


public_key_path = "./public_key.pem"
private_key_path = "./private_key.pem"


def encrypt(message, rsa_public_key):
    buf = io.BytesIO()
    message = message.encode()
    max_block_len = rsa_public_key.size_in_bytes() - 11

    cipher = PKCS1_v1_5.new(rsa_public_key)
    for i in range(0, len(message), max_block_len):
        buf.write(cipher.encrypt(message[i:i+max_block_len]))
    return base64.b64encode(buf.getvalue())


def decrypt(secret_message, rsa_private_key):
    buf = io.BytesIO()
    max_block_len = rsa_private_key.size_in_bytes()
    cipher = PKCS1_v1_5.new(rsa_private_key)
    secret_message = base64.b64decode(secret_message)
    for i in range(0, len(secret_message), max_block_len):
        buf.write(cipher.decrypt(secret_message[i:i+max_block_len], "decrypt_error"))
    return buf.getvalue()


if __name__ == "__main__":
    plain = 'message12345'
    with open(public_key_path) as pub_f, open(private_key_path) as priv_f:
        pub_key = RSA.importKey(pub_f.read())
        priv_key = RSA.importKey(priv_f.read())

    print('raw_msg_len：', len(plain), plain)
    secret = encrypt(plain, pub_key)
    print('secret_msg_len：', len(secret))
    text = decrypt(secret, priv_key)
    print('decrypt_msg_len：', len(text), text)
    assert plain.encode() == text
```

### Python中数据和16进制互转
```
import binascii

# 将bytes转为hex
binascii.b2a_hex(data)

# 将hex转为bytes
binascii.a2b_hex(hex_str)
```

## Java代码
```
package helloworld;

import java.security.Key;
import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

import javax.crypto.Cipher;

public class rsa_demo {

    public String encryptoMode ="RSA/ECB/PKCS1Padding";
    //public String encryptoMode ="RSA/ECB/NoPadding";

    private String sign_str = "私钥字符串";

    private String pubKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3fPGMFICABkczIWrWbUd5yEKU" +
            "KI+jDcJhKXIYEefKGBmZUmKuVw3GN/oK0AP9HggbXeIcXhrlfTPXvucED0GP9A1n" +
            "cQcfNoO3QObWR3HqcFDUUCMpuwclH/xeq/KwcXd4pTUJEWYzHphRdk5cfrMMa/Xr" +
            "HMiN6DLQvXdYU24o6QIDAQAB";

    public String priKey = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALd88YwUgIAGRzMh" +
            "atZtR3nIQpQoj6MNwmEpchgR58oYGZlSYq5XDcY3+grQA/0eCBtd4hxeGuV9M9e+" +
            "5wQPQY/0DWdxBx82g7dA5tZHcepwUNRQIym7ByUf/F6r8rBxd3ilNQkRZjMemFF2" +
            "Tlx+swxr9escyI3oMtC9d1hTbijpAgMBAAECgYEAjz/3YHJ9I/ZCzfNP8pocTEKB" +
            "YCQOh7DtSWfPEGWiPY/1JFNCgXOraE45Ywmlo443rA3uwlDh1Lqbp9r9hpjWiFbu" +
            "MizzxxgrCDQ+rrARLb+EQ8APgQmJKIxJ/eledRYuDbk8DeXVe607ocCLCLEHQnbE" +
            "ckF8DB87y8+J1jDFVvUCQQDeTKOCbMNwrch71HGGpDye4Hn2hWcFHK5pcyz4uhM0" +
            "ksHFh5U9yWJsk96LdVi4sK2ydU5fgsuMbX7rAiheQ4jLAkEA004NKU7ug2y1erEK" +
            "18oxSNXe+V6DCXEmfvcZKBBt8T2yFsqU6i+jVfaBIt9AuY5VTtwlDEFF6sEBpo88" +
            "ixJCmwJAZi+4ogW5OZzJIhMgNJJew3HQ3r+oAbOTgSnOrG9s0Kf9pv2SXxqpwduf" +
            "W2AP7qZY0kYWRtVrGBxlUUZmpB5LTQJAc2kXES/WYBv5Bzk5leEOiBygO42efoK5" +
            "pvEpYVOP6QpsgbxGF57LVIFdyQEtJewStg7RgV8JZA3k6+ciB0eC7wJANt31g0vG" +
            "z4MiF7TUBfqAXxy/iOGLTfVpaYPBR0bmhc9vLydxW2Sx02TPsimMczi3TbwYgOeZ" +
            "udpPXkdMawr8nw==";

    /**
     * 获得公钥
     * @return
     * @throws NoSuchAlgorithmException
     * @throws InvalidKeySpecException
     */
    private PublicKey getPublicKey(String pubKeyString) throws NoSuchAlgorithmException, InvalidKeySpecException {
        byte[] pubKeyByte = Base64.getDecoder().decode(pubKey);
        X509EncodedKeySpec spec = new X509EncodedKeySpec(pubKeyByte);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        PublicKey pubkey = keyFactory.generatePublic(spec);
        return pubkey;
    }
    /**
     * 获得私钥
     * @return
     */
    private PrivateKey getPrivateKey(String priKeyString) throws NoSuchAlgorithmException, InvalidKeySpecException {
        byte[] priKeyByte = Base64.getDecoder().decode(priKey);
        PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(priKeyByte);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        PrivateKey priKey = keyFactory.generatePrivate(spec);
        return priKey;
    }

    /**
     * 公钥加密 （私钥加密）
     */
    public String encrypto(String text,Key key) {
        try{
            Cipher cipher = Cipher.getInstance(encryptoMode);
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte tempBytes[] = cipher.doFinal(text.getBytes());
            String secretText=Base64.getEncoder().encodeToString(tempBytes);
            return secretText;
        }catch(Exception e){
            throw new RuntimeException("加密字符串[" + text + "]时遇到异常", e);
        }
    }
    /**
     * 私钥解密（公钥解密）
     * @param secretText
     */
    public String decrypto(String secretText,Key key) {
        try{
            //生成公钥
            Cipher cipher = Cipher.getInstance(encryptoMode);
            cipher.init(Cipher.DECRYPT_MODE, key);
            // 密文解码
            byte[] secretText_decode = Base64.getDecoder().decode(secretText.getBytes());
            byte tempBytes[] = cipher.doFinal(secretText_decode);
            String text=new String( tempBytes);
            return text;
        }catch(Exception e){
            throw new RuntimeException("解密字符串[" + secretText + "]时遇到异常", e);
        }
    }
    /**
     * 由于每次公钥 加密出来的结果都不一样，所有python java 每次加密出来的结果都不一样，也就没有可比性。我们只考虑能解密就行
     * @param args
     */
    public static void main(String[] args) throws Exception {
        rsa_demo rsa = new rsa_demo();
        System.err.println("明文:"+rsa.sign_str);
        PublicKey pubkey = rsa.getPublicKey(rsa.pubKey);
        PrivateKey prikey = rsa.getPrivateKey(rsa.priKey);
        String secretText = rsa.encrypto(rsa.sign_str,pubkey);//公钥加密，私钥解密

        System.out.println("密文:"+secretText);
        String text =  rsa.decrypto(secretText,prikey);
        System.out.println("明文:"+text);
    }
}
```

## 其他
    需要注意加解密的填充问题，而Python的库m2crypto能够支持NoPadding，这点需要注意，golang的标准库也不支持NoPadding填充方式；和Java程序互通调试的时候一定要注意填充方式问题。
    

## ref
    一些参考资料
    
### RSA
    **是一种非对称加密算法**

    
### PKCS
    **是一种文件标准**
    The Public-Key Cryptography Standards (PKCS)
    是由美国RSA数据安全公司及其合作伙伴制定的一组公钥密码学标准，其中包括证书申请、证书更新、证书作废表发布、扩展证书内容以及数字签名、数字信封的格式等方面的一系列相关协议。

### X509
    **是一种标准**
    X.509是一种非常通用的证书格式。X509就是数字证书的标准，规定了数字证书的格式。在一份证书中，必须证明公钥及其所有者的姓名是一致的。对X.509证书来说，认证者总是CA或由CA指定的人，一份X.509证书是一些标准字段的集合，这些字段包含有关用户或设备及其相应公钥的信息。X.509标准定义了证书中应该包含哪些信息，并描述了这些信息是如何编码的(即数据格式)。
    
### PKCXX系列
    PKCS的各个标准的概要
    
 - PKCS#1：RSA加密标准。PKCS#1定义了RSA公钥函数的基本格式标准，特别是数字签名。它定义了数字签名如何计算，包括待签名数据和签名本身的格式；它也定义了PSA公/私钥的语法。
 - PKCS#2：涉及了RSA的消息摘要加密，这已被并入PKCS#1中。
 - PKCS#3：Diffie-Hellman密钥协议标准。PKCS#3描述了一种实现Diffie-Hellman密钥协议的方法。
 - PKCS#4：最初是规定RSA密钥语法的，现已经被包含进PKCS#1中。
 - PKCS#5：基于口令的加密标准。PKCS#5描述了使用由口令生成的密钥来加密8位位组串并产生一个加密的8位位组串的方法。PKCS#5可以用于加密私钥，以便于密钥的安全传输（这在PKCS#8中描述）。
 - PKCS#6：扩展证书语法标准。PKCS#6定义了提供附加实体信息的X.509证书属性扩展的语法（当PKCS#6第一次发布时，X.509还不支持扩展。这些扩展因此被包括在X.509中）。
 - PKCS#7：密码消息语法标准。PKCS#7为使用密码算法的数据规定了通用语法，比如数字签名和数字信封。PKCS#7提供了许多格式选项，包括未加密或签名的格式化消息、已封装（加密）消息、已签名消息和既经过签名又经过加密的消息。
 - PKCS#8：私钥信息语法标准。PKCS#8定义了私钥信息语法和加密私钥语法，其中私钥加密使用了PKCS#5标准。
 - PKCS#9：可选属性类型。PKCS#9定义了PKCS#6扩展证书、PKCS#7数字签名消息、PKCS#8私钥信息和PKCS#10证书签名请求中要用到的可选属性类型。已定义的证书属性包括E-mail地址、无格式姓名、内容类型、消息摘要、签名时间、签名副本（counter signature）、质询口令字和扩展证书属性。
 - PKCS#10：证书请求语法标准。PKCS#10定义了证书请求的语法。证书请求包含了一个唯一识别名、公钥和可选的一组属性，它们一起被请求证书的实体签名（证书管理协议中的PKIX证书请求消息就是一个PKCS#10）。
 - PKCS#11：密码令牌接口标准。PKCS#11或“Cryptoki”为拥有密码信息（如加密密钥和证书）和执行密码学函数的单用户设备定义了一个应用程序接口（API）。智能卡就是实现Cryptoki的典型设备。注意：Cryptoki定义了密码函数接口，但并未指明设备具体如何实现这些函数。而且Cryptoki只说明了密码接口，并未定义对设备来说可能有用的其他接口，如访问设备的文件系统接口。
 - PKCS#12：个人信息交换语法标准。PKCS#12定义了个人身份信息（包括私钥、证书、各种秘密和扩展字段）的格式。PKCS#12有助于传输证书及对应的私钥，于是用户可以在不同设备间移动他们的个人身份信息。
 - PDCS#13：椭圆曲线密码标准。PKCS#13标准当前正在完善之中。它包括椭圆曲线参数的生成和验证、密钥生成和验证、数字签名和公钥加密，还有密钥协定，以及参数、密钥和方案标识的ASN.1语法。
 - PKCS#14：伪随机数产生标准。PKCS#14标准当前正在完善之中。为什么随机数生成也需要建立自己的标准呢？PKI中用到的许多基本的密码学函数，如密钥生成和Diffie-Hellman共享密钥协商，都需要使用随机数。然而，如果“随机数”不是随机的，而是取自一个可预测的取值集合，那么密码学函数就不再是绝对安全了，因为它的取值被限于一个缩小了的值域中。因此，安全伪随机数的生成对于PKI的安全极为关键。
 - PKCS#15：密码令牌信息语法标准。PKCS#15通过定义令牌上存储的密码对象的通用格式来增进密码令牌的互操作性。在实现PKCS#15的设备上存储的数据对于使用该设备的所有应用程序来说都是一样的，尽管实际上在内部实现时可能所用的格式不同。PKCS#15的实现扮演了翻译家的角色，它在卡的内部格式与应用程序支持的数据格式间进行转换。

### links
    [加密算法和文件格式RSA、X509、PKCSXX]("https://www.zhihu.com/question/22524886")
    [DER,PEM convert]("https://www.poftut.com/convert-der-pem-pem-der-certificate-format-openssl/")
    ```

#!/usr/bin/env python3
"""
SSL/TLS Key Log Extractor and Injector

从PCAP文件中提取SSL随机数，匹配SSL key log文件中的对应密钥，并注入到PCAP文件中。
"""

import argparse
import subprocess
import sys
import os
import tempfile
import logging
from typing import List, Dict, Optional, Set
from datetime import datetime


class SSLKeyLogExtractor:
    """SSL/TLS密钥提取和注入工具"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志配置"""
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def run_command(self, cmd: List[str], description: str = "") -> str:
        """执行命令并打印"""
        cmd_str = ' '.join(cmd)
        self.logger.info(f"执行命令: {cmd_str}")
        if description:
            self.logger.info(f"说明: {description}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                self.logger.error(f"命令执行失败: {result.stderr}")
                return ""
            
            self.logger.info(f"命令执行成功")
            return result.stdout
            
        except subprocess.TimeoutExpired:
            self.logger.error("命令执行超时")
            return ""
        except Exception as e:
            self.logger.error(f"命令执行异常: {e}")
            return ""
    
    def extract_random_numbers_from_pcap(self, pcap_path: str) -> Set[str]:
        """从PCAP文件中提取SSL/TLS随机数"""
        cmd = [
            'tshark', '-r', pcap_path,
            '-Y', '(ssl.handshake.random or tls.handshake.random)',
            '-T', 'fields',
            '-e', 'ssl.handshake.random',
            '-e', 'tls.handshake.random',
            '-E', 'separator=|'
        ]
        
        output = self.run_command(cmd, "从PCAP中提取SSL/TLS随机数")
        if not output:
            return set()
        
        random_numbers = set()
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
            
            fields = line.split('|')
            for field in fields:
                if field and field.strip():
                    random_num = field.strip()
                    if len(random_num) == 64:  # 32 bytes = 64 hex chars
                        random_numbers.add(random_num)
        
        self.logger.info(f"找到 {len(random_numbers)} 个唯一随机数")
        return random_numbers
    
    def parse_ssl_key_log_file(self, keylog_path: str) -> Dict[str, List[Dict]]:
        """解析SSL key log文件并按随机数索引"""
        self.logger.info(f"解析SSL key log文件: {keylog_path}")
        
        if not os.path.exists(keylog_path):
            raise FileNotFoundError(f"SSL key log文件不存在: {keylog_path}")
        
        key_index = {}
        
        try:
            with open(keylog_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 3:
                        label = parts[0]
                        random_num = parts[1]
                        secret = ' '.join(parts[2:])
                        
                        if len(random_num) == 64:
                            if random_num not in key_index:
                                key_index[random_num] = []
                            
                            key_index[random_num].append({
                                'label': label,
                                'random': random_num,
                                'secret': secret,
                                'line_number': line_num
                            })
            
            self.logger.info(f"解析完成，包含 {len(key_index)} 个唯一随机数")
            return key_index
            
        except Exception as e:
            raise Exception(f"解析SSL key log文件失败: {e}")
    
    def match_and_extract_keys(self, pcap_randoms: Set[str], 
                              key_index: Dict[str, List[Dict]]) -> List[Dict]:
        """匹配随机数并提取密钥"""
        self.logger.info("匹配随机数与SSL密钥...")
        
        matched_keys = []
        
        for random_num in pcap_randoms:
            if random_num in key_index:
                for key_entry in key_index[random_num]:
                    matched_keys.append({
                        'type': key_entry['label'],
                        'random': key_entry['random'],
                        'master_secret': key_entry['secret']
                    })
        
        self.logger.info(f"匹配到 {len(matched_keys)} 个密钥条目")
        return matched_keys
    
    def write_key_log_file(self, key_entries: List[Dict], output_path: str) -> bool:
        """写入密钥日志文件"""
        try:
            lines = []
            lines.append("# SSL/TLS Key Log File")
            lines.append(f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")
            
            for entry in key_entries:
                line = f"{entry['type']} {entry['random']} {entry['master_secret']}"
                lines.append(line)
            
            with open(output_path, 'w') as f:
                f.write('\n'.join(lines))
            
            self.logger.info(f"密钥文件已写入: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"写入密钥文件失败: {e}")
            return False
    
    def inject_keys_into_pcap(self, pcap_path: str, key_entries: List[Dict], 
                            output_pcap: str) -> bool:
        """将密钥注入到PCAP文件"""
        if not key_entries:
            self.logger.warning("没有密钥可注入")
            return False
        
        temp_fd, temp_keylog = tempfile.mkstemp(suffix='.log', prefix='ssl_keys_')
        os.close(temp_fd)
        
        try:
            if not self.write_key_log_file(key_entries, temp_keylog):
                return False
            
            cmd = ['editcap', '--inject-secrets', f'tls,{temp_keylog}', pcap_path, output_pcap]
            self.run_command(cmd, f"将 {len(key_entries)} 个密钥注入到PCAP文件")
            
            self.logger.info(f"密钥注入完成: {output_pcap}")
            return True
            
        finally:
            if os.path.exists(temp_keylog):
                os.unlink(temp_keylog)
    
    def extract_and_inject_keys(self, pcap_path: str, keylog_path: str, 
                               output_pcap: str, output_keylog: Optional[str] = None) -> bool:
        """一次性完成提取和注入"""
        self.logger.info("开始一次性提取和注入SSL密钥...")
        
        # 步骤1: 提取随机数
        self.logger.info("步骤 1/3: 从PCAP文件中提取随机数")
        pcap_randoms = self.extract_random_numbers_from_pcap(pcap_path)
        
        if not pcap_randoms:
            raise Exception("在PCAP文件中未找到SSL/TLS随机数")
        
        # 步骤2: 解析SSL key log文件
        self.logger.info("步骤 2/3: 解析SSL key log文件")
        key_index = self.parse_ssl_key_log_file(keylog_path)
        
        # 步骤3: 匹配和注入
        self.logger.info("步骤 3/3: 匹配随机数并注入密钥")
        matched_keys = self.match_and_extract_keys(pcap_randoms, key_index)
        
        if not matched_keys:
            raise Exception("未找到与PCAP中随机数匹配的密钥")
        
        # 保存密钥文件（可选）
        if output_keylog:
            if not self.write_key_log_file(matched_keys, output_keylog):
                raise Exception("写入密钥文件失败")
            self.logger.info(f"匹配的密钥已保存到: {output_keylog}")
        
        # 注入密钥到PCAP
        if not self.inject_keys_into_pcap(pcap_path, matched_keys, output_pcap):
            raise Exception("注入密钥到PCAP文件失败")
        
        self.logger.info("✅ 一次性操作成功完成!")
        self.logger.info(f"   - 匹配到 {len(matched_keys)} 个密钥条目")
        self.logger.info(f"   - 输出PCAP文件: {output_pcap}")
        if output_keylog:
            self.logger.info(f"   - 输出Key Log文件: {output_keylog}")
        
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='SSL/TLS Key Log Extractor and Injector',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s input.pcap -k ssl_keys.log -1 -o output.pcap
  %(prog)s input.pcap -k ssl_keys.log -1 -o output.pcap -s keys.log
  %(prog)s input.pcap --keylog-file ssl_keys.log --one-step --output-pcap output.pcap --save-keys keys.log
        """
    )
    
    parser.add_argument('pcap_file', help='输入PCAP文件')
    parser.add_argument('-k', '--keylog-file', required=True, help='SSL key log文件')
    parser.add_argument('-1', '--one-step', action='store_true', help='一次性完成提取和注入')
    parser.add_argument('-o', '--output-pcap', required=True, help='输出PCAP文件')
    parser.add_argument('-s', '--save-keys', help='保存匹配的密钥到指定文件（可选）')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if not args.one_step:
        parser.error("当前版本只支持 --one-step 模式")
    
    # 初始化提取器
    extractor = SSLKeyLogExtractor(verbose=args.verbose)
    
    try:
        # 执行一次性操作
        success = extractor.extract_and_inject_keys(
            args.pcap_file, 
            args.keylog_file, 
            args.output_pcap,
            args.save_keys
        )
        
        if success:
            print("✅ 操作成功完成!")
        else:
            print("❌ 操作失败!")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
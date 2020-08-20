import os
import argparse
from cryptography.fernet import Fernet

class FileEncryptor(object):

    def parse_args(self):

        parser = argparse.ArgumentParser(
            description = 'Encrypt or decrypt files.'
        )

        parser.add_argument(
            'files',
            nargs = '+',
            help = 'Specify one or more text files.'
        )
        parser.add_argument(
            '-k',
            dest = 'key_file',
            default = 'crypto.key',
            help = 'Specify a key file.'
        )
        parser.add_argument(
            '-d',
            dest = 'decrypt',
            action = 'store_true',
            default = False,
            help = 'Decrypt files.'
        )

        args = parser.parse_args()

        self.files = args.files
        self.key_file = args.key_file
        self.decrypt_bool  = args.decrypt

    def generate_key(self):

        key = Fernet.generate_key()
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)

    def load_key(self):

        if not os.path.exists(self.key_file):
            self.generate_key()
        return open(self.key_file, "rb").read()

    def encrypt_file(self, file):
       
        with open(file, mode='rb') as f:
            content = f.read()        
        
        # content = content.encode()
        content = self.encryptor.encrypt(content)
        
        output = self.add_suffix(file)
        with open(output, mode='wb') as f:
            f.write(content)

    def decrypt_file(self, file):

        with open(file, mode='rb') as f:
            content = f.read()
        
        content = self.encryptor.decrypt(content)
        # content = content.decode()

        output = self.add_suffix(file)
        with open(output, mode='wb') as f:
            f.write(content)

    def add_suffix(self, file):
            basename = os.path.basename(file)
            filename = os.path.splitext(basename)[0]
            extension = os.path.splitext(basename)[1]
            if self.decrypt_bool:
                if '_encrypted' in filename:
                    return filename.replace('_encrypted', '_decrypted') + extension
                else:
                    return filename + '_decrypted' + extension

            else:
                return filename + '_encrypted' + extension

    def determine_task(self):
        
        self.key = self.load_key()
        self.encryptor = Fernet(self.key)
        for f in self.files:        
            if self.decrypt_bool:
                self.decrypt_file(f)
            else:
                self.encrypt_file(f)

if __name__ == "__main__":
    fencryptor = FileEncryptor()
    fencryptor.parse_args()  
    fencryptor.determine_task()  

from Crypto.PublicKey import RSA


class PairGenerator():
    def __init__(self, public, private):
        self.public = public
        self.private = private
        self.key = RSA.generate(2048)

    def generate_private_key(self):
        private_key = self.key.export_key()
        file_out = open(self.private, "wb")
        file_out.write(private_key)

    def generate_public_key(self):
        public_key = self.key.publickey().export_key()
        file_out = open(self.public, "wb")
        file_out.write(public_key)

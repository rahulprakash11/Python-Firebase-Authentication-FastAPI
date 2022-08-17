class MongoDbConstant:

    class AuthProvider:

        class AuthType:
            firebase = 0x1
            
        class Providers:
            google = "google.com"
            phone = "phone"

    class User:
        class Status:
            unverified = 0x1
            unverifiedMask = 0x1
            verified = 0x2
            verifiedMask = 0x2
            statusMask = 0xf

        class Role:
            player = 0x1
            playerMask = 0x1
            admin = 0x2
            adminMask = 0x2
            roleMask = 0xf



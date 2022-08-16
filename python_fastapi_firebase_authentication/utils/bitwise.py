

class Bitwise:
    mask = [0xf, 0xf0, 0xf00, 0xf000]

    def containsValue(self, originalValue:int, maskValue:int, checkFor:int) -> bool:
        n = self.mask.index(maskValue)
        return ((originalValue & maskValue) == (checkFor << 4*n))


    def clearValue(self, value:int, maskValue:int) -> int:
        return ((value & (~maskValue)) & maskValue)


    def attachValue(self, originalValue:int, maskValue:int, attachValue:int) -> int:
        n = self.mask.index(maskValue)
        return ((originalValue & (~maskValue)) | (attachValue << 4*n))

    def getValue(self, originalVal:int, maskVal:int) -> int:
        n = self.mask.index(maskVal)

        return ((originalVal & maskVal) >> 4*n)

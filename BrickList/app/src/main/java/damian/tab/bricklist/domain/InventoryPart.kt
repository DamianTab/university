package damian.tab.bricklist.domain

import android.database.Cursor
import android.graphics.Bitmap

class InventoryPart : SQLParser {

    //    Database
    var id: Int = -1
    var inventoryId: Int = -1
    var typeId: Int = -1
    var itemId: Int = -1
    var quantityInSet: Int = -1
    var quantityInStore: Int = -1
    var colorId: Int = -1

    //    Extra
    var name: String? = null
    var color: String? = null
    var itemCode: String? = null
    var colorCode: Int? = null
    var typeCode: String? = null

    var designCode: Int? = null
    var image: Bitmap? = null

    constructor()
    constructor(
        inventoryId: Int,
        quantityInSet: Int,
        itemCode: String?,
        colorCode: Int?,
        typeCode: String?
    ) {
        this.inventoryId = inventoryId
        this.quantityInStore = 0
        this.quantityInSet = quantityInSet
        this.itemCode = itemCode
        this.colorCode = colorCode
        this.typeCode = typeCode
    }

    override fun parse(cursor: Cursor): InventoryPart {
        this.id = cursor.getInt(0)
        this.inventoryId = cursor.getInt(1)
        this.typeId = cursor.getInt(2)
        this.itemId = cursor.getInt(3)
        this.quantityInSet = cursor.getInt(4)
        this.quantityInStore = cursor.getInt(5)
        this.colorId = cursor.getInt(6)
        return this
    }
}
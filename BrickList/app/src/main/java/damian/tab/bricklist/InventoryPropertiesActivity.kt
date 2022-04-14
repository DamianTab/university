package damian.tab.bricklist

import android.app.Activity
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Switch
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import damian.tab.bricklist.adapter.InventoryPartListAdapter
import damian.tab.bricklist.database.SQLExecutor
import damian.tab.bricklist.domain.Inventory
import damian.tab.bricklist.domain.InventoryPart
import kotlinx.android.synthetic.main.activity_inventory_properties.*
import org.w3c.dom.Document
import org.w3c.dom.Element
import java.io.File
import javax.xml.parsers.DocumentBuilder
import javax.xml.parsers.DocumentBuilderFactory
import javax.xml.transform.OutputKeys
import javax.xml.transform.Transformer
import javax.xml.transform.TransformerFactory
import javax.xml.transform.dom.DOMSource
import javax.xml.transform.stream.StreamResult

class InventoryPropertiesActivity : AppCompatActivity() {

    private lateinit var inventory: Inventory
    private lateinit var inventoryParts: List<InventoryPart>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_inventory_properties)
        SQLExecutor.initialize(this)
        inventory = (intent.extras?.get(INVENTORY_DATA) as Inventory?)!!
        val menuBar = supportActionBar
        menuBar!!.title = inventory.name
        menuBar.subtitle = "Project Name"

        inventoryParts = SQLExecutor.getInventoryParts(inventory.id)
        SQLExecutor.supplyPartsNamesAndColors(inventoryParts)
        SQLExecutor.supplyDesignCodesAndImages(inventoryParts)
        val invalidPartsCount = inventoryParts.filter {
            it.itemId == -1
        }.count()

        if (invalidPartsCount > 0) {
            Toast.makeText(
                this,
                "There is no information about  $invalidPartsCount  brick in database !",
                Toast.LENGTH_LONG
            ).show()
            inventoryParts = inventoryParts.filter {
                it.itemId != -1
            }
        }

        inventory_part_list.adapter = InventoryPartListAdapter(this, inventoryParts)
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.inventory_properties_menu, menu)
        val menuItemView = menu!!.findItem(R.id.properties_archived_switch).actionView
        val switch = menuItemView.findViewById<Switch>(R.id.properties_archived_switch_supplier)
        switch.isChecked = inventory.active == 0
        switch.setOnClickListener {
            inventory.active = if (switch.isChecked) 0 else 1
        }
        return super.onCreateOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        when (item.itemId) {
            R.id.properties_save_button -> {
                save()
            }
            R.id.properties_export_button -> {
                inventory.active = 0
                save()
                exportToXML()
                Toast.makeText(
                    applicationContext,
                    "Export project to file: " + inventory.name + ".xml",
                    Toast.LENGTH_LONG
                ).show()
                finish()
            }
        }
        return super.onOptionsItemSelected(item)
    }

    override fun finish() {
        setResult(Activity.RESULT_OK, intent)
        super.finish()
    }

    private fun save() {
        SQLExecutor.updateInventoryStatusAndAccessDate(inventory)
        inventoryParts.forEach {
            SQLExecutor.updateInventoryPart(it)
        }
        Toast.makeText(
            applicationContext,
            "Project saved.",
            Toast.LENGTH_SHORT
        ).show()
    }

    private fun exportToXML() {
        val docBuilder: DocumentBuilder = DocumentBuilderFactory.newInstance().newDocumentBuilder()
        val doc: Document = docBuilder.newDocument()
        val rootElement: Element = doc.createElement("INVENTORY")
        inventoryParts.forEach {
            val itemNode = doc.createElement("ITEM")
            val typeNode = doc.createElement("ITEMTYPE")
            val idNode = doc.createElement("ITEMID")
            val colorNode = doc.createElement("COLOR")
            val quantityNode = doc.createElement("QTYFILLED")

            val missingQuantity = it.quantityInSet - it.quantityInStore
            if (missingQuantity > 0) {
                quantityNode.textContent = missingQuantity.toString()
                itemNode.appendChild(quantityNode)

                typeNode.textContent = it.typeCode
                itemNode.appendChild(typeNode)

                idNode.textContent = it.itemCode
                itemNode.appendChild(idNode)

                colorNode.textContent = it.colorCode.toString()
                itemNode.appendChild(colorNode)

                rootElement.appendChild(itemNode)
            }

        }
        doc.appendChild(rootElement)
        val transformer: Transformer = TransformerFactory.newInstance().newTransformer()
        transformer.setOutputProperty(OutputKeys.INDENT, "yes")
        transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2")
        val file = File(this.getExternalFilesDir(null), "${inventory.name}.xml")
        transformer.transform(DOMSource(doc), StreamResult(file))
    }
}

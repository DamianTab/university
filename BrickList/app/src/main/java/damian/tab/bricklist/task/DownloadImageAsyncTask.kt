package damian.tab.bricklist.task

import android.graphics.BitmapFactory
import android.os.AsyncTask
import android.widget.ImageView
import damian.tab.bricklist.IMAGE_URL_1
import damian.tab.bricklist.IMAGE_URL_2
import damian.tab.bricklist.IMAGE_URL_3
import damian.tab.bricklist.database.SQLExecutor
import damian.tab.bricklist.domain.InventoryPart
import java.net.URL

class DownloadImageAsyncTask(
    private val part: InventoryPart,
    private val imageView: ImageView
) : AsyncTask<String, Void, Void>() {

    override fun doInBackground(vararg params: String?): Void? {
        var url = URL(IMAGE_URL_1 + part.designCode)
        try {
            downloadImage(url)
            if (part.image != null) SQLExecutor.updateImageInBLOB(part)
        } catch (e: Exception) {
            url =
                if (part.colorCode == null || part.colorCode == 0) URL(IMAGE_URL_2 + part.itemCode + ".jpg")
                else URL(IMAGE_URL_3 + part.colorCode + "/" + part.itemCode + ".jpg")
            try {
//              No design code so we can't save in database
                downloadImage(url)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        return null
    }

    override fun onPostExecute(result: Void?) {
        if (part.image != null) imageView.setImageBitmap(part.image)
    }

    private fun downloadImage(url: URL) {
        url.openConnection().getInputStream().use {
            part.image = BitmapFactory.decodeStream(it)
        }
    }
}
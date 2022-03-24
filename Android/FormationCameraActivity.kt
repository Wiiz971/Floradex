package fr.wiiz.floradex.floradex_identification

import android.app.Activity
import android.graphics.Camera
import android.graphics.PixelFormat
import android.os.Bundle
import android.view.SurfaceHolder
import android.view.SurfaceView
import android.view.Window
import android.view.WindowManager
import java.io.IOException
import android.hardware.Camera


class FormationCameraActivity : Activity(), SurfaceHolder.Callback {

    private var camera: android.hardware.Camera? = null
    private var surfaceCamera: SurfaceView? = null
    private var isPreview: Boolean? = null
    override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {

        // Si le mode preview est lancé alors nous le stoppons
        if (isPreview!!) {
            camera!!.stopPreview()
        }
        // Nous récupérons les paramètres de la caméra
        val params = mCamera.getParameters()

        // Nous changeons la taille
        parameters.setPreviewSize(width, height)

        // Nous appliquons nos nouveaux paramètres
        camera!!.setParameters(parameters)

        try {
            // Nous attachons notre prévisualisation de la caméra au holder de la
            // surface
            camera!!.setPreviewDisplay(surfaceCamera!!.holder)
        } catch (e: IOException) {
        }

        // Nous lançons la preview
        camera!!.startPreview()

        isPreview = true
    }

    override fun surfaceCreated(holder: SurfaceHolder) {
        // Nous arrêtons la camera et nous rendons la main
        if (camera != null) {
            camera!!.stopPreview()
            isPreview = false
            camera!!.release()
        }
    }

    override fun surfaceDestroyed(holder: SurfaceHolder) {
        // Nous prenons le contrôle de la camera
        if (camera == null)
            camera = Camera.open()
    }

    public override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Nous mettons l'application en plein écran et sans barre de titre
        window.setFormat(PixelFormat.TRANSLUCENT)
        requestWindowFeature(Window.FEATURE_NO_TITLE)
        window.setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        )

        isPreview = false

        // Nous appliquons notre layout
        setContentView(R.layout.main)

        // Nous récupérons notre surface pour le preview
        surfaceCamera = findViewById(R.id.surfaceViewCamera) as SurfaceView

        // Méthode d'initialisation de la caméra
        InitializeCamera()

        surfaceCamera!!.setOnClickListener(object : OnClickListener() {

            fun onClick(v: View) {
                // Nous prenons une photo
                if (camera != null) {
                    SavePicture()
                }

            }
        })
        // Callback pour la prise de photo
        val pictureCallback = object : Camera.PictureCallback() {

            fun onPictureTaken(data: ByteArray?, camera: Camera) {
                if (data != null) {
                    // Enregistrement de votre image
                    try {
                        if (stream != null) {
                            stream.write(data)
                            stream.flush()
                            stream.close()
                        }
                    } catch (e: Exception) {
                        // TODO: handle exception
                    }

                    // Nous redémarrons la prévisualisation
                    camera.startPreview()
                }
            }
        }
    }

    public override fun onResume() {
        super.onResume()
        camera = Camera.open()
    }

    // Mise en pause de l'application
    public override fun onPause() {
        super.onPause()

        if (camera != null) {
            camera!!.release()
            camera = null
        }
    }

    private fun InitializeCamera() {
        // Nous attachons nos retours du holder à notre activité
        surfaceCamera!!.holder.addCallback(this)
        // Nous spécifiions le type du holder en mode SURFACE_TYPE_PUSH_BUFFERS
        surfaceCamera!!.holder.setType(
            SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS
        )
    }

    private fun SavePicture() {
        try {
            val timeStampFormat = SimpleDateFormat(
                "yyyy-MM-dd-HH.mm.ss"
            )
            val fileName = ("photo_" + timeStampFormat.format(Date())
                    + ".jpg")

            // Metadata pour la photo
            val values = ContentValues()
            values.put(Media.TITLE, fileName)
            values.put(Media.DISPLAY_NAME, fileName)
            values.put(Media.DESCRIPTION, "Image prise par FormationCamera")
            values.put(Media.DATE_TAKEN, Date().getTime())
            values.put(Media.MIME_TYPE, "image/jpeg")

            // Support de stockage
            val taken = contentResolver.insert(
                Media.EXTERNAL_CONTENT_URI,
                values
            )

            // Ouverture du flux pour la sauvegarde
            stream = contentResolver.openOutputStream(
                taken!!
            ) as FileOutputStream

            camera!!.takePicture(null, pictureCallback, pictureCallback)
        } catch (e: Exception) {
            // TODO: handle exception
        }

    }


}

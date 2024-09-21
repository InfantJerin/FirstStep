package com.senpro.firststep

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.PopupMenu
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.view.WindowCompat
import androidx.recyclerview.widget.LinearLayoutManager
import com.senpro.firststep.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var speechRecognizer: SpeechRecognizer
    private val REQUEST_RECORD_AUDIO_PERMISSION = 200

    private var currentLanguage = "English";

    private val messages = mutableListOf<Message>()
    private lateinit var messageAdapter: MessageAdapter

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        WindowCompat.setDecorFitsSystemWindows(window, false)

        // Check and request permissions
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.RECORD_AUDIO),
                REQUEST_RECORD_AUDIO_PERMISSION
            )
        }

        // Initialize SpeechRecognizer
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
        speechRecognizer.setRecognitionListener(recognitionListener)

        // Set up RecyclerView
        messageAdapter = MessageAdapter(messages)
        binding.recyclerView.adapter = messageAdapter
        binding.recyclerView.layoutManager = LinearLayoutManager(this)

        // Set up FAB click listener
        binding.fab.setOnClickListener {
            startSpeechToText()
        }

        // Retrieve messages from database
        val dbHelper = MessageDbHelper(this)
        messages.addAll(dbHelper.getMessages())
        messageAdapter.notifyItemRangeInserted(0, messages.size)

        binding.recyclerView.scrollToPosition(messages.size - 1)

        val popupMenu = PopupMenu(this, binding.languageChooser)
        popupMenu.inflate(R.menu.language_menu)
        popupMenu.setOnMenuItemClickListener { item ->
            var response = false
            when (item.itemId) {
                R.id.english -> {
                    currentLanguage = "English"
                    response = true
                }
                R.id.bengali -> {
                    currentLanguage = "Bengali"
                    response = true
                }
                R.id.hindi -> {
                    currentLanguage = "Hindi"
                    response = true
                }
                R.id.tamil -> {
                    currentLanguage = "Tamil"
                    response = true
                }
                else -> response = true
            }
            binding.languageChooser.text = currentLanguage
            response
        }

        binding.languageChooser.setOnClickListener {
            popupMenu.show()
        }

        binding.languageChooser.text = currentLanguage
    }

    private fun startSpeechToText() {
        val languageCode = getLanguageCode(currentLanguage)

        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(
                RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, languageCode)
        }
        speechRecognizer.startListening(intent)
    }

    private fun getLanguageCode(language: String): String {
        return when (language) {
            "English" -> "en-US"
            "Bengali" -> "bn-IN"
            "Hindi" -> "hi-IN"
            "Tamil" -> "ta-IN"
            else -> "en-US"
        }
    }

    private val recognitionListener = object : RecognitionListener {
        override fun onReadyForSpeech(params: Bundle?) {}
        override fun onBeginningOfSpeech() {
            binding.fab.setImageResource(R.drawable.ic_stop)
        }

        override fun onRmsChanged(rmsdB: Float) {}
        override fun onBufferReceived(buffer: ByteArray?) {}
        override fun onEndOfSpeech() {
            binding.fab.setImageResource(android.R.drawable.ic_btn_speak_now)
        }

        override fun onError(error: Int) {
            Toast.makeText(this@MainActivity, "Error occurred", Toast.LENGTH_SHORT).show()
        }

        override fun onResults(results: Bundle?) {
            val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
            if (matches != null && matches.isNotEmpty()) {
                addMessage(matches[0], true)
            }
        }

        override fun onPartialResults(partialResults: Bundle?) {}
        override fun onEvent(eventType: Int, params: Bundle?) {}
    }

    private fun addMessage(text: String, isUser: Boolean) {
        val message = Message(text, isUser)
        messages.add(message)
        messageAdapter.notifyItemInserted(messages.size - 1)
        binding.recyclerView.scrollToPosition(messages.size - 1)

        // Store in database
        val dbHelper = MessageDbHelper(this)
        dbHelper.addMessage(message)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_RECORD_AUDIO_PERMISSION) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permission granted
            } else {
                // Permission denied
                Toast.makeText(
                    this,
                    "Record audio permission denied",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        speechRecognizer.destroy()
    }
}
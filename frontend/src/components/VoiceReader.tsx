import { useState, useEffect } from "react";
import { Volume2, VolumeX, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Language } from "@/lib/translations";

interface VoiceReaderProps {
  text: string;
  language: Language;
}

export const VoiceReader = ({ text, language }: VoiceReaderProps) => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Check if browser supports speech synthesis
    if (!('speechSynthesis' in window)) {
      console.warn('Speech synthesis not supported');
      setIsSupported(false);
    }

    // Stop speech when component unmounts or text changes
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, [text]);

  const speak = async () => {
    console.log('Voice button clicked', { 
      isSupported, 
      isSpeaking, 
      textLength: text.length,
      textPreview: text.substring(0, 100) 
    });
    
    if (!isSupported) {
      console.warn('Speech not supported');
      return;
    }

    // If already speaking, stop
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();
    
    setIsLoading(true);
    setIsSpeaking(true);

    try {
      // For very long text, limit to first 500 characters for better performance
      const textToSpeak = text.length > 500 ? text.substring(0, 500) + "..." : text;
      
      console.log('Text to speak:', textToSpeak.substring(0, 100));

      // Create speech synthesis utterance
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      
      // Set language
      utterance.lang = language === "te" ? "te-IN" : "en-US";
      
      // Configure speech parameters
      utterance.rate = 0.85; // Slower for better comprehension
      utterance.pitch = 1.0;
      utterance.volume = 1.0;

      // Event handlers
      utterance.onstart = () => {
        console.log('Speech started successfully');
        setIsLoading(false);
      };

      utterance.onend = () => {
        console.log('Speech ended');
        setIsSpeaking(false);
      };

      utterance.onerror = (event) => {
        console.error('Speech synthesis error:', event.error, event);
        setIsSpeaking(false);
        setIsLoading(false);
        alert(`Speech error: ${event.error}. Try shorter text or check browser permissions.`);
      };

      utterance.onpause = () => {
        console.log('Speech paused');
      };

      utterance.onresume = () => {
        console.log('Speech resumed');
      };

      // Wait for voices to load
      const loadVoices = () => {
        return new Promise<void>((resolve) => {
          const voices = window.speechSynthesis.getVoices();
          
          if (voices.length > 0) {
            console.log('Available voices:', voices.length, voices.map(v => `${v.name} (${v.lang})`));
            
            if (language === "te") {
              // Try to find Telugu voice
              const teluguVoice = voices.find(voice => 
                voice.lang.includes('te') || 
                voice.name.toLowerCase().includes('telugu')
              );
              if (teluguVoice) {
                console.log('Using Telugu voice:', teluguVoice.name);
                utterance.voice = teluguVoice;
              } else {
                console.log('No Telugu voice found. Available:', voices.filter(v => v.lang.startsWith('te')));
              }
            } else {
              // Try to find English voice
              const englishVoice = voices.find(voice => 
                voice.lang === 'en-IN' || 
                voice.lang === 'en-US' ||
                voice.lang.startsWith('en')
              );
              if (englishVoice) {
                console.log('Using English voice:', englishVoice.name);
                utterance.voice = englishVoice;
              }
            }
            resolve();
          } else {
            console.log('No voices available yet, waiting...');
            window.speechSynthesis.onvoiceschanged = () => {
              console.log('Voices changed event fired');
              loadVoices().then(resolve);
            };
          }
        });
      };

      // Load voices and then speak
      await loadVoices();
      
      // Start speaking
      console.log('Calling speechSynthesis.speak()...');
      window.speechSynthesis.speak(utterance);
      
      // Fallback: if speech doesn't start in 2 seconds, show error
      setTimeout(() => {
        if (isLoading) {
          console.error('Speech did not start within 2 seconds');
          setIsLoading(false);
          setIsSpeaking(false);
        }
      }, 2000);
      
    } catch (error) {
      console.error('Error in speak function:', error);
      setIsLoading(false);
      setIsSpeaking(false);
      alert('Speech failed. Please try again.');
    }
  };

  if (!isSupported) {
    return null; // Don't show button if not supported
  }

  return (
    <Button
      variant={isSpeaking ? "destructive" : "outline"}
      size="sm"
      onClick={speak}
      disabled={isLoading}
      className="gap-2 shrink-0"
    >
      {isLoading ? (
        <>
          <Loader2 className="h-4 w-4 animate-spin" />
          <span className="hidden sm:inline">
            {language === "en" ? "Loading..." : "లోడ్ అవుతోంది..."}
          </span>
        </>
      ) : isSpeaking ? (
        <>
          <VolumeX className="h-4 w-4" />
          <span className="hidden sm:inline">
            {language === "en" ? "Stop" : "ఆపు"}
          </span>
        </>
      ) : (
        <>
          <Volume2 className="h-4 w-4" />
          <span className="hidden sm:inline">
            {language === "en" ? "Read Aloud" : "చదవండి"}
          </span>
        </>
      )}
    </Button>
  );
};
;

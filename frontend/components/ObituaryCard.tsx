"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Trash2, Calendar, Volume2, Download, Loader2 } from "lucide-react";
import type { Obituary } from "@/types/obituary";
import { formatDate } from "@/lib/utils";
import { useState } from "react";

interface ObituaryCardProps {
  obituary: Obituary;
  onDelete?: (id: string) => void;
  showActions?: boolean;
}

export default function ObituaryCard({
  obituary,
  onDelete,
  showActions = false,
}: ObituaryCardProps) {
  const [isAudioLoading, setIsAudioLoading] = useState(false);

  const handleDownloadAudio = () => {
    if (obituary.audio_url) {
      const link = document.createElement('a');
      link.href = obituary.audio_url;
      link.download = `${obituary.name.replace(/\s+/g, '_')}_obituary.mp3`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <CardTitle className="text-2xl">{obituary.name}</CardTitle>
            <CardDescription className="flex items-center gap-2 mt-2">
              <Calendar className="w-4 h-4" />
              {formatDate(obituary.birth_date)} -{" "}
              {formatDate(obituary.death_date)}
            </CardDescription>
          </div>
          {showActions && onDelete && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete(obituary.id)}
              className="text-red-600 hover:text-red-700 hover:bg-red-50"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {obituary.image_url && obituary.image_url.startsWith('http') && (
          <div className="w-full h-48 rounded-md overflow-hidden bg-gray-100">
            <img
              src={obituary.image_url}
              alt={obituary.name}
              className="w-full h-full object-cover"
              onError={(e) => {
                // Hide image if it fails to load
                e.currentTarget.parentElement!.style.display = 'none';
              }}
            />
          </div>
        )}

        <div className="prose prose-sm max-w-none">
          <p className="text-sm text-gray-700 whitespace-pre-line leading-relaxed">
            {obituary.obituary_text}
          </p>
        </div>

        {/* Text-to-Speech Audio Player */}
        {obituary.audio_url ? (
          <div className="pt-4 border-t bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <Volume2 className="w-5 h-5 text-purple-600" />
              <p className="text-sm font-semibold text-gray-900">
                Listen to Obituary
              </p>
            </div>

            <audio
              controls
              className="w-full mb-3"
              onLoadStart={() => setIsAudioLoading(true)}
              onCanPlay={() => setIsAudioLoading(false)}
              onError={() => setIsAudioLoading(false)}
            >
              <source src={obituary.audio_url} type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>

            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownloadAudio}
                className="flex items-center gap-2 text-xs"
              >
                <Download className="w-3 h-3" />
                Download Audio
              </Button>
              <p className="text-xs text-gray-500 flex items-center">
                Powered by Amazon Polly
              </p>
            </div>
          </div>
        ) : (
          <div className="pt-4 border-t bg-gray-50 rounded-lg p-4">
            <div className="flex items-center gap-2 text-gray-500">
              <Loader2 className="w-4 h-4 animate-spin" />
              <p className="text-sm">Generating audio narration...</p>
            </div>
          </div>
        )}

        <div className="text-xs text-muted-foreground pt-2 border-t">
          <span>Created on {formatDate(obituary.created_at)}</span>
        </div>
      </CardContent>
    </Card>
  );
}

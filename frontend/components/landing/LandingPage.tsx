import Link from "next/link";

import FeatureCard from "./FeatureCard";

const LandingPage = () => {
  return (
    <div
      className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900
  to-slate-900 p-4"
    >
      {/* Animated background */}
      <div className="absolute inset-0 overflow-hidden">
        <div
          className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter
  blur-xl opacity-20 animate-blob"
        ></div>
        <div
          className="absolute -bottom-40 -left-40 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter
  blur-xl opacity-20 animate-blob animation-delay-2000"
        ></div>
      </div>

      {/* Landing Content */}
      <div className="relative text-center max-w-4xl">
        <h1 className="text-6xl md:text-8xl font-bold text-white mb-6 tracking-tight">
          The Last Show
        </h1>
        <p className="text-xl md:text-2xl text-purple-200 mb-12 max-w-2xl mx-auto">
          AI-powered obituary generator. Create beautiful, heartfelt tributes
          with the help of artificial intelligence.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/register"
            className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg
  shadow-lg hover:shadow-purple-500/50 hover:scale-105 transition-all duration-200"
          >
            Get Started
          </Link>
          <Link
            href="/login"
            className="px-8 py-4 bg-white/10 backdrop-blur-lg text-white font-semibold rounded-lg border
  border-white/20 hover:bg-white/20 transition-all duration-200"
          >
            Sign In
          </Link>
        </div>

        {/* Features */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6">
          <FeatureCard
            icon="🤖"
            title="AI-Powered"
            description="Generate meaningful obituaries using AI"
          />
          <FeatureCard
            icon="🎙️"
            title="Text-to-Speech"
            description="Convert obituaries to audio with Amazon Polly"
          />
          <FeatureCard
            icon="📸"
            title="Media Storage"
            description="Store photos and audio securely in the cloud"
          />
        </div>
      </div>
    </div>
  );
};

export default LandingPage;

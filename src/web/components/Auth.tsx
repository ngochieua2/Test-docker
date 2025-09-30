// components/auth/Login.tsx - Updated for Custom JWT
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/authContext";

// Logo Component
const Logo = ({ className }: { className?: string }) => (
  <svg
    className={className}
    width="89"
    height="75"
    viewBox="0 0 89 75"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M24.0537 0.0224609C32.5332 0.0224588 41.0167 -0.051534 49.4941 0.0693359C52.6491 0.113659 55.8773 0.27625 58.9336 0.983398C65.4851 2.50044 71.3273 5.4945 76.3135 10.1562C80.5583 14.1251 83.7092 18.7953 85.8428 24.124C86.7372 26.3602 87.1766 28.8079 87.5996 31.1992C87.9723 33.3106 88.202 35.4747 88.208 37.6162C88.2362 46.2229 85.313 53.7901 80.0527 60.5654C76.92 64.6007 72.9852 67.6735 68.6416 70.1455C66.0409 71.6261 63.0533 72.5165 60.1484 73.3545C55.8794 74.5855 51.4546 74.7326 47.0264 74.6963C42.1309 74.658 37.2334 74.702 32.3379 74.708C30.4905 74.71 30.3133 74.5331 30.2871 72.6133C30.2569 70.3428 30.0391 68.0539 30.2607 65.8096C30.567 62.705 28.5942 61.0068 26.7891 59.0586C25.1169 57.2535 23.179 56.5558 20.7695 56.7754C19.4177 56.8983 18.0456 56.7817 16.6816 56.7979C15.5576 56.8099 15.0136 56.2984 15.0176 55.1562C15.0277 51.6245 15.0517 48.0903 14.9912 44.5586C14.9711 43.3863 15.4668 43.0703 16.5264 43.1045C18.2912 43.1589 20.0603 43.1162 21.8271 43.1484C23.2393 43.1746 24.4684 42.8547 25.4736 41.7549C26.6361 40.4856 28.0099 39.3928 29.0615 38.043C29.6598 37.2734 30.0473 36.1577 30.0957 35.1787C30.2307 32.3583 30.1885 29.5276 30.124 26.7031C30.0958 25.448 30.5929 24.9782 31.8057 24.9883C36.3991 25.0225 40.9906 25.0366 45.584 25.0205C46.5307 25.0165 46.8008 25.4395 46.7969 26.3096C46.7707 30.9513 46.7683 35.5955 46.7764 40.2393C46.7764 41.2607 46.3331 41.6859 45.3057 41.6758C42.5296 41.6476 39.7536 41.6758 36.9775 41.6758C35.5814 41.6758 34.3903 41.9416 33.4414 43.1807C32.6214 44.2504 31.4493 45.0429 30.5205 46.0381C28.5644 48.1374 28.1817 51.133 30.3574 53.3994C31.4936 54.584 32.5388 55.918 33.8623 56.8447C34.9059 57.576 36.3004 58.1175 37.5615 58.1699C41.7439 58.3412 45.9385 58.2506 50.1289 58.2627C54.6921 58.2768 59.0659 57.2206 62.7588 54.6318C66.3046 52.1478 69.0572 48.8743 70.54 44.5488C71.5131 41.7082 72.0207 38.9275 71.8213 35.9922C71.4525 30.5709 69.1091 26.1027 65.2129 22.3555C62.8658 20.099 60.0107 18.7388 57.0693 17.5703C55.6571 17.0083 54.0513 16.7037 52.5283 16.6855C44.6049 16.5929 36.6774 16.6057 28.7539 16.6621C27.8614 16.6682 26.7345 16.9336 26.124 17.5098C24.319 19.2101 22.681 21.0937 21.0693 22.9854C20.7329 23.3802 20.6985 24.1122 20.6885 24.6924C20.6482 26.9567 20.6728 29.2231 20.6729 31.7715L20.667 31.7637H12.7471C11.2326 31.7644 9.71809 31.7682 8.2041 31.7803C7.44665 31.7863 6.96078 31.6751 6.96875 30.7324C7.00098 26.8965 6.99286 23.0624 6.9707 19.2266C6.96667 18.3926 7.25901 18.0618 8.12305 18.0879C9.78716 18.1403 11.456 18.0721 13.1201 18.1104C15.0923 18.1566 16.7178 17.4251 17.999 15.9707C19.2542 14.5443 20.512 13.1076 21.6221 11.5684C22.0147 11.0224 22.1012 10.1683 22.1133 9.44922C22.1636 6.38089 22.1357 3.3124 22.1357 0.0224609H24.0537ZM10.6514 10.7451H0V6.25586C0.00403033 4.59582 0.0280201 2.93543 0.00585938 1.27539C-0.00613641 0.47991 0.282304 0.0303777 1.12207 0.0302734H10.6514V10.7451Z"
      fill="url(#paint0_linear_84_2772)"
    />
    <defs>
      <linearGradient
        id="paint0_linear_84_2772"
        x1="0"
        y1="37.354"
        x2="88.2082"
        y2="37.354"
        gradientUnits="userSpaceOnUse"
      >
        <stop stopColor="#F8B738" />
        <stop offset="1" stopColor="#F95085" />
      </linearGradient>
    </defs>
  </svg>
);

// Google Icon Component
const GoogleIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 24 24">
    <path
      fill="#4285f4"
      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
    />
    <path
      fill="#34a853"
      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
    />
    <path
      fill="#fbbc05"
      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
    />
    <path
      fill="#ea4335"
      d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
    />
  </svg>
);

interface LoginProps {
  mode?: "signin" | "signup";
  onToggleMode?: () => void;
  tenant?: string; // Add tenant prop
}

export default function Login({
  mode = "signin",
  onToggleMode,
  tenant,
}: LoginProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const router = useRouter();
  const { login, register, loginWithGoogle } = useAuth();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      if (mode === "signup") {
        // Register new user
        const result = await register({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          tenant: tenant || "default",
        });

        if (result.success) {
          // Redirect to email verification page
          router.push(
            `/auth/verify-email?email=${encodeURIComponent(formData.email)}`
          );
        } else {
          setError(result.error || "Failed to create account");
        }
      } else {
        // Sign in existing user
        const result = await login({
          email: formData.email,
          password: formData.password,
          tenant: tenant || "default",
        });

        if (result.success) {
          // Redirect to dashboard with tenant context
          router.push("/dashboard");
        } else {
          setError(result.error || "Invalid email or password");
        }
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : "Something went wrong");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    try {
      setIsLoading(true);
      const result = await loginWithGoogle({
        tenant: tenant || "default",
      });

      if (result.success) {
        router.push("/dashboard");
      } else {
        setError(result.error || "Failed to sign in with Google");
      }
    } catch (error) {
      setError("Failed to sign in with Google");
    } finally {
      setIsLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const isSignUp = mode === "signup";

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 flex items-center justify-center p-5">
      <div className="bg-white rounded-2xl shadow-2xl p-10 w-full max-w-md border border-gray-100">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <Logo className="w-16 h-auto" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2 tracking-tight">
            Data Cooking
          </h1>
          {tenant && (
            <p className="text-sm text-gray-500 mb-2">
              Signing in to{" "}
              <span className="font-semibold text-orange-500">{tenant}</span>
            </p>
          )}
          <p className="text-lg text-gray-600 font-medium">
            {isSignUp ? "Let's create an account" : "Welcome back"}
          </p>
        </div>

        {/* Google Sign In Button */}
        <button
          onClick={handleGoogleSignIn}
          disabled={isLoading}
          className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-gray-300 rounded-lg bg-white text-gray-700 hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 mb-6 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <GoogleIcon />
          Continue with Google
        </button>

        {/* Divider */}
        <div className="flex items-center gap-4 mb-6">
          <div className="flex-1 h-px bg-gray-300"></div>
          <span className="text-gray-500 text-sm font-medium">or</span>
          <div className="flex-1 h-px bg-gray-300"></div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Name Field (Sign Up Only) */}
          {isSignUp && (
            <div>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Name or Company Name"
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 focus:bg-white focus:border-orange-400 focus:ring-2 focus:ring-orange-100 focus:outline-none transition-all duration-200 text-gray-900 placeholder-gray-500"
              />
            </div>
          )}

          {/* Email Field */}
          <div>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="Email"
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 focus:bg-white focus:border-orange-400 focus:ring-2 focus:ring-orange-100 focus:outline-none transition-all duration-200 text-gray-900 placeholder-gray-500"
            />
          </div>

          {/* Password Field */}
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Password"
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 focus:bg-white focus:border-orange-400 focus:ring-2 focus:ring-orange-100 focus:outline-none transition-all duration-200 text-gray-900 placeholder-gray-500 pr-12"
            />
            <button
              type="button"
              onClick={togglePasswordVisibility}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors duration-200 p-1"
            >
              {showPassword ? (
                <span className="text-sm">🙈</span>
              ) : (
                <span className="text-sm">👁</span>
              )}
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3">
              <p className="text-red-600 text-sm text-center">{error}</p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-orange-400 to-pink-500 text-white py-3 rounded-lg font-semibold hover:shadow-lg hover:from-orange-500 hover:to-pink-600 transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {isLoading ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Loading...
              </div>
            ) : isSignUp ? (
              "Continue with Email"
            ) : (
              "Sign In"
            )}
          </button>
        </form>

        {/* Toggle Mode */}
        <div className="text-center mt-6">
          <p className="text-gray-600 text-sm">
            {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
            {onToggleMode ? (
              <button
                onClick={onToggleMode}
                className="text-orange-500 hover:text-orange-600 font-semibold transition-colors duration-200"
              >
                {isSignUp ? "Sign In" : "Sign Up"}
              </button>
            ) : (
              <a
                href={isSignUp ? "/auth/signin" : "/auth/signup"}
                className="text-orange-500 hover:text-orange-600 font-semibold transition-colors duration-200"
              >
                {isSignUp ? "Sign In" : "Sign Up"}
              </a>
            )}
          </p>
        </div>

        {/* Additional Links */}
        {isSignUp ? (
          <div className="text-center mt-6">
            <p className="text-xs text-gray-500 leading-relaxed">
              By continuing, you agree to our{" "}
              <a
                href="/terms"
                className="text-orange-500 hover:text-orange-600 hover:underline transition-colors duration-200"
              >
                Terms & Conditions
              </a>{" "}
              and{" "}
              <a
                href="/privacy"
                className="text-orange-500 hover:text-orange-600 hover:underline transition-colors duration-200"
              >
                Privacy Policy
              </a>
            </p>
          </div>
        ) : (
          <div className="text-center mt-4">
            <a
              href="/auth/forgot-password"
              className="text-orange-500 hover:text-orange-600 text-sm font-medium transition-colors duration-200"
            >
              Forgot password?
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

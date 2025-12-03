"use client";

import { useState, useTransition } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  obituaryCreateSchema,
  type ObituaryCreateInput,
} from "@/lib/schemas/obituary.schema";
import { createObituaryAction } from "@/app/actions/obituary";

interface CreateObituaryFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess?: () => void;
}

export default function CreateObituaryForm({
  open,
  onOpenChange,
  onSuccess,
}: CreateObituaryFormProps) {
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [creationStage, setCreationStage] = useState<string>("");

  const form = useForm<ObituaryCreateInput>({
    resolver: zodResolver(obituaryCreateSchema),
    defaultValues: {
      name: "",
      birth_date: "",
      death_date: "",
      is_public: false,
    },
  });

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const onSubmit = async (data: ObituaryCreateInput) => {
    setError(null);

    console.log(" React Hook Form data:", data);
    const formValues = {
      name: data.name,
      birth_date: data.birth_date,
      death_date: data.death_date,
      is_public: data.is_public, // boolean
    };

    // Validate with Zod
    const parsed = obituaryCreateSchema.safeParse(formValues);
    if (!parsed.success) {
      console.error(" Validation errors:", parsed.error.format());
      setError("Please check the form fields and try again.");
      return;
    }

    // Append to FormData
    const formData = new FormData();
    Object.entries(parsed.data).forEach(([key, value]) => {
      formData.append(
        key,
        key === "is_public" ? (value ? "true" : "false") : String(value)
      );
    });

    if (selectedImage) {
      console.log(" Appending image:", selectedImage.name);
      formData.append("image", selectedImage);
    }

    console.log(" Final FormData contents:");
    for (const [key, value] of formData.entries()) {
      console.log("   ", key, "=>", value);
    }

    startTransition(async () => {
      try {
        setCreationStage("Generating AI obituary text...");
        await new Promise((resolve) => setTimeout(resolve, 500));

        const result = await createObituaryAction(formData);
        console.log(" Raw result from server action:", result);

        setCreationStage("Uploading image and generating audio...");

        if (result.success) {
          console.log(" Obituary created successfully:", result);
          setCreationStage("");
          form.reset();
          setSelectedImage(null);
          setImagePreview(null);
          if (onSuccess) onSuccess();
        } else {
          setCreationStage("");
          console.error(
            " Server-side error:",
            result.error,
            result.fieldErrors
          );
          if (result.fieldErrors) {
            const messages = Object.values(result.fieldErrors)
              .flat()
              .join(", ");
            setError(messages || result.error);
          } else {
            setError(result.error || "An unknown error occurred.");
          }
        }
      } catch (err) {
        setCreationStage("");
        console.error(" Network or unexpected error:", err);
        setError("Network error or server is unreachable.");
      }
    });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent onClose={() => onOpenChange(false)}>
        <DialogHeader>
          <DialogTitle>Create New Obituary</DialogTitle>
          <DialogDescription>
            Fill in the details below to generate an AI-powered obituary
          </DialogDescription>
        </DialogHeader>
        <div className="p-6 pt-0">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              {error && (
                <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm">
                  {error}
                </div>
              )}

              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Full Name *</FormLabel>
                    <FormControl>
                      <Input placeholder="John Doe" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="birth_date"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Birth Date *</FormLabel>
                      <FormControl>
                        <Input type="date" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="death_date"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Death Date *</FormLabel>
                      <FormControl>
                        <Input type="date" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="space-y-2">
                <FormLabel>Photo (Optional)</FormLabel>
                <Input
                  id="image"
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="cursor-pointer"
                />
                {imagePreview && (
                  <div className="mt-2">
                    <img
                      src={imagePreview}
                      alt="Preview"
                      className="w-32 h-32 object-cover rounded-md border"
                    />
                  </div>
                )}
                <p className="text-xs text-muted-foreground">
                  Image upload will be available after AWS setup
                </p>
              </div>

              {/* All obituaries are private by default */}

              {isPending && creationStage && (
                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                  <div className="flex items-center gap-3">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-600"></div>
                    <div>
                      <p className="text-sm font-medium text-purple-900">
                        {creationStage}
                      </p>
                      <p className="text-xs text-purple-600 mt-1">
                        This may take 30-60 seconds for audio generation
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <Button type="submit" className="w-full" disabled={isPending}>
                {isPending ? (
                  <span className="flex items-center gap-2">
                    <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
                    Creating Obituary...
                  </span>
                ) : (
                  "Generate Obituary"
                )}
              </Button>
            </form>
          </Form>
        </div>
      </DialogContent>
    </Dialog>
  );
}

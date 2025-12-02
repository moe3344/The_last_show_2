"use server";

import { revalidatePath } from "next/cache";
import { serverAPI } from "@/lib/server-api";
import { getErrorMessage } from "@/types/errors";
import { obituaryCreateSchema } from "@/lib/schemas/obituary.schema";

export async function deleteObituaryAction(id: string) {
  try {
    await serverAPI.deleteObituary(id);
    // Revalidate the dashboard path to refetch the obituaries list
    revalidatePath("/dashboard");
    return { success: true };
  } catch (err) {
    return { success: false, error: getErrorMessage(err) };
  }
}

export async function createObituaryAction(formData: FormData) {
  console.log("🚀 createObituaryAction called");

  // Get the values from FormData
  const name = formData.get("name") as string;
  const birth_date = formData.get("birth_date") as string;
  const death_date = formData.get("death_date") as string;
  const is_public_str = formData.get("is_public") as string;
  const image = formData.get("image") as File | null;

  // Convert is_public string to boolean
  const is_public = is_public_str === "true";

  console.log("📦 Parsed data:", { name, birth_date, death_date, is_public, image: image?.name });

  // Validate the data (excluding image)
  const validatedFields = obituaryCreateSchema.safeParse({
    name,
    birth_date,
    death_date,
    is_public,
  });

  if (!validatedFields.success) {
    console.log("❌ Validation errors:", validatedFields.error.format());
    return {
      success: false,
      error: "Invalid form data. Please check the fields and try again.",
      fieldErrors: validatedFields.error.flatten().fieldErrors,
    };
  }

  try {
    // Create FormData for the API call
    const apiFormData = new FormData();
    apiFormData.append("name", validatedFields.data.name);
    apiFormData.append("birth_date", validatedFields.data.birth_date);
    apiFormData.append("death_date", validatedFields.data.death_date);
    apiFormData.append("is_public", String(validatedFields.data.is_public));

    if (image && image.size > 0) {
      apiFormData.append("image", image);
    }

    console.log("📤 Sending to backend...");
    await serverAPI.createObituary(apiFormData);

    revalidatePath("/dashboard");
    console.log("✅ Obituary created successfully");
    return { success: true };
  } catch (err) {
    console.error("❌ Error creating obituary:", err);
    return { success: false, error: getErrorMessage(err) };
  }
}

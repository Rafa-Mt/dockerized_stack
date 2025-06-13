import { ref } from "vue";
import type { Ref } from "vue";


interface SuperQueryResult<T> {
  data: Ref<T | null>;
  error: Ref<string | null>;
  loading: Ref<boolean>;
}

export async function useSuperQuery<T>(url: string, options: RequestInit = {}) {
  const resultData = ref<T | null>(null);
  const resultError = ref<string | null>(null);
  const resultLoading = ref<boolean>(true);

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    resultData.value = (await response.json()) as T;
  } catch (error) {
    resultError.value = error instanceof Error ? error.message : String(error);
  } finally {
    resultLoading.value = false;
  }

  return {
    data: resultData,
    error: resultError,
    loading: resultLoading,
  } as SuperQueryResult<T>;


}


interface SuperMutationResult<T> {
  mutate: (data: T) => Promise<void>;
  mutating?: Ref<boolean>;
}

export function useSuperMutation<Request, Response>(
{ url, onSuccess, onError, options = {} }: { url: string; onSuccess?: (data: Response) => void; onError?: (error: Error) => void; options?: RequestInit; }): SuperMutationResult<Request> {
  
  const mutating = ref<boolean>(false);
  const mutate = async (data: Request) => {
    mutating.value = true;
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        body: JSON.stringify(data),
        ...options,
      });
      mutating.value = false
      if (!response.ok) {
        const errorText = await response.text();
        const error = new Error(`HTTP error! status: ${response.status} - ${errorText}`);
        if (onError) {
          onError(error);
        }
      }

      const responseData = (await response.json()) as Response;
      if (onSuccess) {
        onSuccess(responseData);
      }
    } catch (error) {
      mutating.value = false;
      if (onError) {
        onError(error instanceof Error ? error : new Error(String(error)));
      }
    }
  };

  return { mutate };
}
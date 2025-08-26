import { useQuery, useMutation, UseQueryOptions, UseMutationOptions } from '@tanstack/react-query';
import { ClientApi } from './index';

export const useApi = () => {
  const api = ClientApi.rawService;

  const useGet = <T>(
    key: string[],
    url: string,
    options?: UseQueryOptions<T>
  ) => {
    return useQuery<T>({
      queryKey: key,
      queryFn: () => api.get<T>(url),
      ...options,
    });
  };

  const usePost = <T, D = any>(
    options?: UseMutationOptions<T, Error, D>
  ) => {
    return useMutation<T, Error, D>(options);
  };

  const usePut = <T, D = any>(
    options?: UseMutationOptions<T, Error, D>
  ) => {
    return useMutation<T, Error, D>(options);
  };

  const useDelete = <T>(
    options?: UseMutationOptions<T, Error, string>
  ) => {
    return useMutation<T, Error, string>(options);
  };

  return {
    useGet,
    usePost,
    usePut,
    useDelete,
    api,
  };
};
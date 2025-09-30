"use client";

import React, {
  useState,
  useCallback,
  ChangeEvent,
  DragEvent,
  useEffect,
} from "react";
import {
  Upload,
  Plus,
  Search,
  MoreHorizontal,
  X,
  User,
  MessageCircle,
  Send,
  Menu,
  PanelRightOpen,
} from "lucide-react";

// Types
interface UploadedFile {
  file: File;
  name: string;
  size: number;
  type: string;
}

interface DataProfile {
  overview?: {
    total_records?: number;
    columns?: string[];
  };
  preview_rows?: Record<string, unknown>[];
  known_dimensions?: Record<
    string,
    {
      unique: number;
    }
  >;
}

interface Dataset {
  id: string;
  name: string;
  fileName: string;
  sheets: number;
  rows: number;
  columns: number;
  description: string;
  data: Record<string, unknown>[];
  isImported?: boolean;
  profile?: DataProfile; // Added to store the detailed profile data
}

interface ImportResponse {
  success: boolean;
  dataset: Dataset;
  message?: string;
}

interface Project {
  id: string;
  name: string;
  datasets: Dataset[];
}

interface ChatMessage {
  id: string;
  type: "user" | "assistant";
  content: string;
  timestamp: Date;
}

type TabType = "Data" | "Assets";

const uploadFileToBackend = async (
  file: File,
  threadId: string = "ae938e51-0b9d-4f41-bc36-afdc1ec0ce51",
  userId: string = "1a20a69d-b3ae-4d5d-8c05-82a614c0f802",
  apiEndpoint: string = "/api/import-data"
): Promise<ImportResponse> => {
  try {
    const fileBase64 = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        const base64 = result.split(",")[1];
        resolve(base64);
      };
      reader.onerror = () => reject(reader.error);
      reader.readAsDataURL(file);
    });

    const payload = {
      file_base64: fileBase64,
      filename: file.name,
      fileUrl: "",
      thread_id: threadId,
      user_id: userId,
    };

    const response = await fetch(apiEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    // Handle the updated API response structure
    if (result.success && result.data) {
      const apiData = result.data;

      return {
        success: true,
        dataset: {
          id: apiData.dataset_id || `imported-${Date.now()}`,
          name: file.name.replace(/\.[^/.]+$/, ""),
          fileName: apiData.filename || file.name,
          sheets: apiData.sheets || 1,
          rows: apiData.rows || apiData.profile?.overview?.total_records || 0,
          columns:
            apiData.columns || apiData.profile?.overview?.columns?.length || 0,
          description:
            apiData.data_summary ||
            apiData.description ||
            `Imported dataset from ${file.name}`,
          data: apiData.profile?.preview_rows || apiData.processedData || [],
          isImported: true,
          profile: apiData.profile, // Store the full profile for detailed analysis
        },
      };
    } else {
      return {
        success: false,
        dataset: {} as Dataset,
        message: result.message || "Failed to process file",
      };
    }
  } catch (error) {
    console.error("Upload failed:", error);

    return {
      success: false,
      dataset: {} as Dataset,
      message:
        error instanceof Error
          ? `Failed to process file: ${error.message}`
          : "Failed to process file. Please try again.",
    };
  }
};

// Mock API function for sample data
const fetchProjectData = async (): Promise<Project> => {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Sample CSV-like data
  const sampleData: Record<string, unknown>[] = [
    {
      id: 1,
      name: "John Doe",
      age: 28,
      department: "Engineering",
      salary: 85000,
      performance: "Excellent",
    },
    {
      id: 2,
      name: "Jane Smith",
      age: 32,
      department: "Marketing",
      salary: 75000,
      performance: "Good",
    },
    {
      id: 3,
      name: "Mike Johnson",
      age: 45,
      department: "Sales",
      salary: 90000,
      performance: "Excellent",
    },
    {
      id: 4,
      name: "Sarah Wilson",
      age: 29,
      department: "HR",
      salary: 65000,
      performance: "Good",
    },
    {
      id: 5,
      name: "David Brown",
      age: 38,
      department: "Engineering",
      salary: 95000,
      performance: "Excellent",
    },
    {
      id: 6,
      name: "Lisa Davis",
      age: 26,
      department: "Marketing",
      salary: 70000,
      performance: "Average",
    },
    {
      id: 7,
      name: "Tom Miller",
      age: 41,
      department: "Sales",
      salary: 88000,
      performance: "Good",
    },
    {
      id: 8,
      name: "Anna Garcia",
      age: 33,
      department: "Engineering",
      salary: 92000,
      performance: "Excellent",
    },
    {
      id: 9,
      name: "Chris Lee",
      age: 27,
      department: "HR",
      salary: 62000,
      performance: "Good",
    },
    {
      id: 10,
      name: "Emma Taylor",
      age: 35,
      department: "Marketing",
      salary: 78000,
      performance: "Good",
    },
    {
      id: 11,
      name: "Ryan White",
      age: 30,
      department: "Sales",
      salary: 85000,
      performance: "Average",
    },
    {
      id: 12,
      name: "Sophie Clark",
      age: 42,
      department: "Engineering",
      salary: 98000,
      performance: "Excellent",
    },
    {
      id: 13,
      name: "James Rodriguez",
      age: 39,
      department: "Marketing",
      salary: 82000,
      performance: "Good",
    },
    {
      id: 14,
      name: "Olivia Martinez",
      age: 31,
      department: "HR",
      salary: 68000,
      performance: "Good",
    },
    {
      id: 15,
      name: "Daniel Anderson",
      age: 44,
      department: "Sales",
      salary: 91000,
      performance: "Excellent",
    },
    {
      id: 16,
      name: "Grace Thompson",
      age: 28,
      department: "Engineering",
      salary: 87000,
      performance: "Good",
    },
    {
      id: 17,
      name: "Kevin Moore",
      age: 37,
      department: "Marketing",
      salary: 76000,
      performance: "Average",
    },
    {
      id: 18,
      name: "Mia Jackson",
      age: 25,
      department: "HR",
      salary: 58000,
      performance: "Good",
    },
    {
      id: 19,
      name: "Alex Harris",
      age: 40,
      department: "Sales",
      salary: 89000,
      performance: "Excellent",
    },
    {
      id: 20,
      name: "Zoe Martin",
      age: 34,
      department: "Engineering",
      salary: 93000,
      performance: "Excellent",
    },
  ];

  return {
    id: "project-1",
    name: "New project 1",
    datasets: [
      {
        id: "dataset-1",
        name: "dataset 1 name",
        fileName: "employees.csv",
        sheets: 1,
        rows: 20,
        columns: 6,
        description:
          "(This is sample imported file's description generated by AI). Description should also show important insights about the data structure and key findings.",
        data: sampleData,
      },
      {
        id: "dataset-2",
        name: "dataset 2 name",
        fileName: "ROAS_Marketing.xlsx",
        sheets: 1,
        rows: 1240,
        columns: 12,
        description:
          "(This is sample imported file's description generated by AI). Description should also show key marketing metrics and performance indicators.",
        data: sampleData.slice(0, 10),
      },
      {
        id: "dataset-3",
        name: "dataset 3 name",
        fileName: "sales_data.csv",
        sheets: 1,
        rows: 850,
        columns: 8,
        description:
          "(This is sample imported file's description generated by AI). Description should also show sales trends and regional performance data.",
        data: sampleData.slice(0, 8),
      },
    ],
  };
};

const DataAnalysisDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>("Data");
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [project, setProject] = useState<Project | null>(null);
  const [selectedDataset, setSelectedDataset] = useState<Dataset | null>(null);
  const [showDatasetModal, setShowDatasetModal] = useState<boolean>(false);
  const [showUserMenu, setShowUserMenu] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>("");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      type: "assistant",
      content:
        "Hello! I can help you analyze your data. What would you like to know about your datasets?",
      timestamp: new Date(),
    },
  ]);
  const [showMobileChat, setShowMobileChat] = useState<boolean>(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [showImportModal, setShowImportModal] = useState<boolean>(false);
  const [showMobileMenu, setShowMobileMenu] = useState<boolean>(false);

  // Load project data on component mount
  useEffect(() => {
    const loadProjectData = async () => {
      try {
        const projectData = await fetchProjectData();
        setProject(projectData);
        setIsLoading(false);
      } catch (error) {
        console.error("Failed to load project data:", error);
        setIsLoading(false);
      }
    };

    loadProjectData();
  }, []);

  const handleFileUpload = useCallback(
    async (event: ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (!file) return;

      // Validate file type
      const allowedTypes = [
        "text/csv",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      ];

      if (
        !allowedTypes.includes(file.type) &&
        !file.name.match(/\.(csv|xlsx|xls)$/i)
      ) {
        setUploadError(
          "Please upload a valid CSV or Excel file (.csv, .xlsx, .xls)"
        );
        return;
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setUploadError("File size must be less than 10MB");
        return;
      }

      setUploadError(null);
      setUploadedFile({
        file,
        name: file.name,
        size: file.size,
        type: file.type,
      });
      setIsProcessing(true);
      setShowImportModal(false);

      try {
        const result = await uploadFileToBackend(file);

        if (result.success && project) {
          console.log(project, result.dataset);
          setProject((prev) => {
            if (!prev) return null;

            // If there are imported datasets, remove sample datasets and add only the new imported one
            const updatedDatasets = [
              ...prev.datasets.filter((dataset) => dataset.isImported),
              result.dataset,
            ];

            return {
              ...prev,
              datasets: updatedDatasets,
            };
          });
        } else {
          setUploadError(result.message || "Failed to import file");
        }
      } catch (error) {
        setUploadError("An error occurred while importing the file");
        console.error("Import error:", error);
      } finally {
        setIsProcessing(false);
      }

      // Reset file input
      if (event.target) {
        event.target.value = "";
      }
    },
    [project]
  );

  const handleSampleUpload = useCallback(
    (event: ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
        const uploadedFileData: UploadedFile = {
          file,
          name: file.name,
          size: file.size,
          type: file.type,
        };
        setUploadedFile(uploadedFileData);
        setIsProcessing(true);

        // Simulate processing and add to datasets
        setTimeout(() => {
          if (project) {
            const newDataset: Dataset = {
              id: `dataset-${Date.now()}`,
              name: `dataset ${project.datasets.length + 1} name`,
              fileName: file.name,
              sheets: 1,
              rows: 100,
              columns: 5,
              description:
                "(This is sample imported file's description generated by AI). Description should also show key insights from the uploaded data.",
              data: [],
              isImported: false,
            };

            setProject((prev) =>
              prev
                ? {
                    ...prev,
                    datasets: [...prev.datasets, newDataset],
                  }
                : null
            );
          }
          setIsProcessing(false);
        }, 2000);
      }
    },
    [project]
  );

  const handleDragOver = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    async (e: DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      e.stopPropagation();

      const files = e.dataTransfer.files;
      if (!files[0]) return;

      const file = files[0];

      // Validate file type
      const allowedTypes = [
        "text/csv",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      ];

      if (
        !allowedTypes.includes(file.type) &&
        !file.name.match(/\.(csv|xlsx|xls)$/i)
      ) {
        setUploadError(
          "Please upload a valid CSV or Excel file (.csv, .xlsx, .xls)"
        );
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        setUploadError("File size must be less than 10MB");
        return;
      }

      setUploadError(null);
      setUploadedFile({
        file,
        name: file.name,
        size: file.size,
        type: file.type,
      });
      setIsProcessing(true);

      try {
        const result = await uploadFileToBackend(file);

        if (result.success && project) {
          setProject((prev) => {
            if (!prev) return null;

            // Check if there are any imported datasets
            const hasImportedDatasets = prev.datasets.some(
              (dataset) => dataset.isImported
            );

            // If there are imported datasets, remove sample datasets and add only the new imported one
            const updatedDatasets = hasImportedDatasets
              ? [
                  ...prev.datasets.filter((dataset) => dataset.isImported),
                  result.dataset,
                ]
              : [...prev.datasets, result.dataset];

            return {
              ...prev,
              datasets: updatedDatasets,
            };
          });
        } else {
          setUploadError(result.message || "Failed to import file");
        }
      } catch (error) {
        setUploadError("An error occurred while importing the file");
        console.error("Import error:", error);
      } finally {
        setIsProcessing(false);
      }
    },
    [project]
  );

  const handleTabChange = useCallback((tab: TabType) => {
    setActiveTab(tab);
  }, []);

  const openDatasetModal = (dataset: Dataset) => {
    setSelectedDataset(dataset);
    setShowDatasetModal(true);
  };

  const closeDatasetModal = () => {
    setShowDatasetModal(false);
    setSelectedDataset(null);
  };

  const handleSendMessage = () => {
    if (!queryText.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: "user",
      content: queryText,
      timestamp: new Date(),
    };

    setChatMessages((prev) => [...prev, userMessage]);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: `I can help you analyze that data. Based on your query "${queryText}", here are some insights from your datasets...`,
        timestamp: new Date(),
      };
      setChatMessages((prev) => [...prev, aiResponse]);
    }, 1000);

    setQueryText("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      {/* Mobile Menu Overlay */}
      {showMobileMenu && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="fixed inset-0 bg-black/50"
            onClick={() => setShowMobileMenu(false)}
          />
          <div className="fixed top-0 left-0 h-full w-80 bg-white shadow-xl transform transition-transform duration-300 ease-in-out">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold">Menu</h2>
                <button
                  onClick={() => setShowMobileMenu(false)}
                  className="p-2 hover:bg-gray-100 rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-4">
                <div className="pb-4 border-b border-gray-200">
                  <p className="font-medium text-gray-900 mb-2">Hoang Nguyen</p>
                  <p className="text-sm text-gray-600">hoang@example.com</p>
                </div>

                <div className="space-y-2">
                  <button
                    onClick={() => setShowMobileMenu(false)}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded"
                  >
                    New project
                  </button>
                  <button
                    onClick={() => setShowMobileMenu(false)}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded"
                  >
                    All projects
                  </button>
                  <button
                    onClick={() => setShowMobileMenu(false)}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded"
                  >
                    Settings
                  </button>
                </div>

                <div className="pt-4 border-t border-gray-200">
                  <button
                    onClick={() => setShowMobileMenu(false)}
                    className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded"
                  >
                    Log out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Content - Left Side */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header - Fixed */}
        <div className="bg-white border-b border-gray-200 px-4 lg:px-6 py-4 flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3 lg:space-x-4">
              {/* Mobile Menu Button - Show on mobile */}
              <button
                onClick={() => setShowMobileMenu(true)}
                className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
              >
                <Menu className="w-5 h-5" />
              </button>

              {/* Desktop User Menu Button - Hide on mobile */}
              <div className="relative hidden lg:block">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="w-10 h-10 bg-gray-800 text-white rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors"
                >
                  <User className="w-5 h-5" />
                </button>

                {showUserMenu && (
                  <div className="absolute top-full left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-20">
                    <div className="p-3 border-b border-gray-100">
                      <p className="font-medium text-gray-900">Hoang Nguyen</p>
                    </div>
                    <div className="py-1">
                      <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50">
                        New project
                      </button>
                      <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50">
                        All projects
                      </button>
                      <hr className="my-1 border-gray-100" />
                      <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50">
                        Log out
                      </button>
                    </div>
                  </div>
                )}
              </div>

              <span className="text-lg font-medium text-gray-900 truncate">
                {project?.name}
              </span>
            </div>

            {/* Mobile Chat Button */}
            <button
              onClick={() => setShowMobileChat(true)}
              className="lg:hidden p-2 hover:bg-gray-100 rounded-lg relative"
            >
              <PanelRightOpen className="w-5 h-5" />
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-blue-600 rounded-full"></span>
            </button>
          </div>
        </div>

        {/* Tabs - Fixed */}
        <div className="bg-white border-b border-gray-200 flex-shrink-0">
          <div className="flex px-4 lg:px-6 overflow-x-auto">
            <button
              onClick={() => handleTabChange("Data")}
              className={`px-4 py-3 text-sm font-medium border-b-2 whitespace-nowrap ${
                activeTab === "Data"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              Data
            </button>
            <button
              onClick={() => handleTabChange("Assets")}
              className={`px-4 py-3 text-sm font-medium border-b-2 whitespace-nowrap ${
                activeTab === "Assets"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              Assets
            </button>
          </div>
        </div>

        {/* Content Area - Scrollable */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-4 lg:p-6">
            {activeTab === "Data" && (
              <div>
                {/* Toolbar */}
                <div className="flex flex-col sm:flex-row gap-3 mb-6">
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setShowImportModal(true)}
                      className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      <Upload className="w-4 h-4" />
                      <span className="text-sm font-medium">Import Data</span>
                    </button>

                    <input
                      type="file"
                      accept=".csv,.xlsx,.xls"
                      onChange={handleSampleUpload}
                      className="hidden"
                      id="file-upload"
                      disabled={isProcessing}
                    />
                    <label htmlFor="file-upload" className="cursor-pointer">
                      <div className="flex items-center space-x-2 px-3 py-2 bg-white border border-gray-300 rounded-md hover:bg-gray-50">
                        <Plus className="w-4 h-4" />
                        <span className="text-sm text-gray-700">
                          Add Sample
                        </span>
                      </div>
                    </label>

                    <button className="flex items-center space-x-2 px-3 py-2 bg-white border border-gray-300 rounded-md hover:bg-gray-50">
                      <Search className="w-4 h-4" />
                      <span className="text-sm text-gray-700">Search</span>
                    </button>
                  </div>

                  {/* Error Message */}
                  {uploadError && (
                    <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                      <p className="text-sm text-red-600">{uploadError}</p>
                      <button
                        onClick={() => setUploadError(null)}
                        className="text-red-500 hover:text-red-700 text-xs mt-1"
                      >
                        Dismiss
                      </button>
                    </div>
                  )}
                </div>

                {/* Datasets */}
                <div className="space-y-4">
                  {project?.datasets.map((dataset) => (
                    <div
                      key={dataset.id}
                      className="bg-white rounded-lg border border-gray-200 p-4"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <h3 className="font-medium text-gray-900">
                            {dataset.name}
                          </h3>
                          {dataset.isImported && (
                            <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full font-medium">
                              Imported
                            </span>
                          )}
                          {!dataset.isImported && (
                            <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-medium">
                              Sample
                            </span>
                          )}
                        </div>
                        <button className="p-1 hover:bg-gray-100 rounded">
                          <MoreHorizontal className="w-4 h-4 text-gray-400" />
                        </button>
                      </div>

                      {/* Data Table Preview */}
                      <div className="overflow-x-auto mb-3">
                        <table className="min-w-full text-xs">
                          <thead>
                            <tr className="bg-gray-50">
                              {dataset.data.length > 0 &&
                                Object.keys(dataset.data[0]).map(
                                  (header, idx) => (
                                    <th
                                      key={idx}
                                      className="px-2 py-1 text-left text-gray-600 font-medium"
                                    >
                                      {header}
                                    </th>
                                  )
                                )}
                            </tr>
                          </thead>
                          <tbody>
                            {dataset.data.map((row, rowIdx) => (
                              <tr
                                key={rowIdx}
                                className="border-t border-gray-100"
                              >
                                {Object.values(row).map((cell, cellIdx) => (
                                  <td
                                    key={cellIdx}
                                    className="px-2 py-1 text-gray-700"
                                  >
                                    {String(cell)}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>

                      <p className="text-xs text-gray-500 mb-3">
                        {dataset.description}
                      </p>

                      <button
                        onClick={() => openDatasetModal(dataset)}
                        className="text-xs text-blue-600 hover:text-blue-700 font-medium"
                      >
                        View Details
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === "Assets" && (
              <div className="text-center py-12">
                <p className="text-gray-500">Assets view - Coming soon</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Desktop Chat Panel - Right Side - Hidden on mobile */}
      <div className="hidden lg:flex w-[28rem] bg-white border-l border-gray-200 flex-col h-screen flex-shrink-0">
        {/* Chat Header */}
        <div className="px-6 py-4 border-b border-gray-200 flex-shrink-0">
          <div className="flex items-center space-x-3">
            <MessageCircle className="w-6 h-6 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">
              Data Assistant
            </h3>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 min-h-0">
          {chatMessages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.type === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[20rem] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                  message.type === "user"
                    ? "bg-blue-600 text-white rounded-br-md"
                    : "bg-gray-100 text-gray-900 rounded-bl-md"
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
        </div>

        {/* Chat Input */}
        <div className="p-6 border-t border-gray-200 flex-shrink-0">
          <div className="space-y-3">
            {/* Tags */}
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-blue-100 text-blue-700 text-sm rounded-full font-medium">
                @Sales month 10.
              </span>
              <span className="px-3 py-1 bg-blue-100 text-blue-700 text-sm rounded-full font-medium">
                @Sales month 10.
              </span>
            </div>

            {/* Input */}
            <div className="flex space-x-3">
              <textarea
                value={queryText}
                onChange={(e) => setQueryText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="I want to..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-xl resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm leading-relaxed min-h-[3rem]"
                rows={2}
              />
              <button
                onClick={handleSendMessage}
                disabled={!queryText.trim()}
                className="px-4 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex-shrink-0"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Chat Drawer */}
      {showMobileChat && (
        <div className="fixed inset-0 z-50 lg:hidden">
          {/* Lighter backdrop or no backdrop */}
          <div
            className="fixed inset-0 bg-black/20"
            onClick={() => setShowMobileChat(false)}
          />
          <div className="fixed inset-y-0 right-0 w-full max-w-sm bg-white shadow-xl transform transition-transform duration-300 ease-in-out flex flex-col">
            {/* Mobile Chat Header */}
            <div className="px-4 py-4 border-b border-gray-200 flex-shrink-0">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <MessageCircle className="w-6 h-6 text-blue-600" />
                  <h3 className="text-lg font-semibold text-gray-900">
                    Data Assistant
                  </h3>
                </div>
                <button
                  onClick={() => setShowMobileChat(false)}
                  className="p-2 hover:bg-gray-100 rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Mobile Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
              {chatMessages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.type === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[16rem] px-3 py-2 rounded-2xl text-sm leading-relaxed ${
                      message.type === "user"
                        ? "bg-blue-600 text-white rounded-br-md"
                        : "bg-gray-100 text-gray-900 rounded-bl-md"
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))}
            </div>

            {/* Mobile Chat Input */}
            <div className="p-4 border-t border-gray-200 flex-shrink-0">
              <div className="space-y-3">
                {/* Tags */}
                <div className="flex flex-wrap gap-2">
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-medium">
                    @Sales month 10.
                  </span>
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-medium">
                    @Sales month 10.
                  </span>
                </div>

                {/* Input */}
                <div className="flex space-x-2">
                  <textarea
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="I want to..."
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm leading-relaxed min-h-[2.5rem]"
                    rows={2}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={!queryText.trim()}
                    className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex-shrink-0"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Import Modal */}
      {showImportModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full">
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
              <h2 className="text-lg font-medium">Import Your Data</h2>
              <button
                onClick={() => setShowImportModal(false)}
                className="p-1 hover:bg-gray-100 rounded"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6">
              <div
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors"
              >
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Upload your dataset
                </h3>
                <p className="text-gray-600 mb-4">
                  Drag and drop your file here, or click to browse
                </p>

                <input
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="modal-file-upload"
                  disabled={isProcessing}
                />
                <label
                  htmlFor="modal-file-upload"
                  className="cursor-pointer inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Choose File
                </label>

                <div className="mt-4 text-sm text-gray-500">
                  <p>Supported formats: CSV, Excel (.xlsx, .xls)</p>
                  <p>Maximum file size: 10MB</p>
                </div>
              </div>

              {uploadError && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-sm text-red-600">{uploadError}</p>
                </div>
              )}

              <div className="mt-6 flex justify-end space-x-3">
                <button
                  onClick={() => setShowImportModal(false)}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Dataset Modal */}
      {showDatasetModal && selectedDataset && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
              <h2 className="text-lg font-medium">{selectedDataset.name}</h2>
              <button
                onClick={closeDatasetModal}
                className="p-1 hover:bg-gray-100 rounded"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4">
              <div className="mb-4">
                <h3 className="font-medium mb-2">File Info</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• File Name: {selectedDataset.fileName}</li>
                  <li>• Total Sheets: {selectedDataset.sheets}</li>
                  <li>• Total Rows: {selectedDataset.rows.toLocaleString()}</li>
                  <li>• Total Columns: {selectedDataset.columns}</li>
                </ul>
              </div>

              {/* Show additional profile info for imported datasets */}
              {selectedDataset.profile && (
                <div className="mb-4">
                  <h3 className="font-medium mb-2">Data Profile</h3>
                  <div className="bg-gray-50 p-3 rounded-lg text-sm">
                    {selectedDataset.profile.overview && (
                      <div className="mb-2">
                        <strong>Columns:</strong>{" "}
                        {selectedDataset.profile.overview.columns?.join(", ")}
                      </div>
                    )}
                    {selectedDataset.profile.known_dimensions && (
                      <div className="space-y-1">
                        {Object.entries(
                          selectedDataset.profile.known_dimensions
                        ).map(([key, value]) => (
                          <div key={key}>
                            <strong>{key}:</strong> {value.unique} unique values
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div className="mb-4">
                <button className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded hover:bg-gray-200">
                  Clone dataset
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="min-w-full text-sm">
                  <thead>
                    <tr className="bg-gray-50">
                      {selectedDataset.data.length > 0 &&
                        Object.keys(selectedDataset.data[0]).map(
                          (header, idx) => (
                            <th
                              key={idx}
                              className="px-3 py-2 text-left text-gray-600 font-medium"
                            >
                              {header}
                            </th>
                          )
                        )}
                    </tr>
                  </thead>
                  <tbody>
                    {selectedDataset.data.map((row, rowIdx) => (
                      <tr
                        key={rowIdx}
                        className="border-t border-gray-100 hover:bg-gray-50"
                      >
                        {Object.values(row).map((cell, cellIdx) => (
                          <td key={cellIdx} className="px-3 py-2 text-gray-700">
                            {String(cell)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Processing Overlay */}
      {isProcessing && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 text-center max-w-sm mx-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <h3 className="text-lg font-medium text-gray-800 mb-2">
              Processing your file...
            </h3>
            <p className="text-gray-600 text-sm mb-2">
              {uploadedFile ? `Analyzing ${uploadedFile.name}` : "Please wait"}
            </p>
            <div className="text-xs text-gray-500">
              <p>• Parsing file structure</p>
              <p>• Analyzing data quality</p>
              <p>• Generating insights</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataAnalysisDashboard;
